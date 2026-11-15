import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path

from src import PlannerConfig, RRT, RRTStar, load_environment
from src.utils import validate_path


def main():
    parser = argparse.ArgumentParser(description="RRT and RRT* path planning in 2D")
    parser.add_argument("--map", default="simple", help="simple, complex, narrow or a JSON map file")
    parser.add_argument("--algorithm", choices=("rrt", "rrt-star", "both"), default="both")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=2500)
    parser.add_argument("--step-size", type=float, default=0.8)
    parser.add_argument("--goal-bias", type=float, default=0.05)
    parser.add_argument("--robot-radius", type=float, default=0.2)
    parser.add_argument("--goal-radius", type=float)
    parser.add_argument("--gamma", type=float)
    parser.add_argument("--start", type=float, nargs=2)
    parser.add_argument("--goal", type=float, nargs=2)
    parser.add_argument("--stop-on-first", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--save", type=Path, help="Save the final plot as a PNG")
    parser.add_argument("--json", type=Path, help="Save paths, metrics and settings")
    parser.add_argument("--stride", type=int, default=25, help="Iterations per interactive update")
    args = parser.parse_args()

    if args.seed < 0 or args.stride <= 0:
        parser.error("seed >= 0 and stride > 0 are required")
    if args.interactive and (args.save or args.json):
        parser.error("Use the Save PNG button in interactive mode, or omit --interactive to export")

    try:
        environment = load_environment(args.map)
        if args.start:
            environment = replace(environment, start=tuple(args.start))
        if args.goal:
            environment = replace(environment, goal=tuple(args.goal))
        config = PlannerConfig(
            step_size=args.step_size,
            goal_sample_rate=args.goal_bias,
            max_iterations=args.iterations,
            robot_radius=args.robot_radius,
            goal_radius=args.goal_radius,
            neighbor_gamma=args.gamma,
            stop_on_first=args.stop_on_first,
        )
        environment.validate_query(config.robot_radius)
    except (ValueError, FileNotFoundError, KeyError, TypeError) as error:
        parser.error(str(error))

    algorithms = {
        "rrt": [RRT],
        "rrt-star": [RRTStar],
        "both": [RRT, RRTStar],
    }[args.algorithm]

    def create_planners(seed):
        return [algorithm(environment, config, seed) for algorithm in algorithms]

    if not args.interactive:
        import matplotlib
        matplotlib.use("Agg")
    from src.visualization import Simulation, save_snapshot

    if args.interactive:
        Simulation(create_planners, args.seed, args.stride).show()
        return

    planners = create_planners(args.seed)
    results = []
    for planner in planners:
        result = planner.run()
        if result.success and not validate_path(result.path, environment, config.robot_radius):
            raise ValueError("Planner returned an invalid path")

        data = asdict(result)
        data["path"] = result.path.tolist() if result.path is not None else None
        results.append(data)
        length = "no path" if result.path_length is None else f"{result.path_length:.3f} m"
        print(
            f"{result.algorithm}: {length} | {result.planning_time:.3f} s | "
            f"{result.iterations} iterations | {result.number_of_nodes} nodes"
        )

    if args.save:
        save_snapshot(planners, args.save)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({
            "environment": environment.to_dict(),
            "config": asdict(config),
            "results": results,
        }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

