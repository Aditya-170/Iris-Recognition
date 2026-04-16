import os
import random
import sys
import numpy as np
import time

# Rich UI
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich import box

# Import your existing functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'iris_recoginition'))
from iris_recoginition.utils.extractandenconding import extractFeature, HammingDistance

console = Console()

THRESHOLD = 0.47
IMPOSTOR_USERS_SAMPLE = 30

VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

# ============================
# Feature Cache
# ============================
feature_cache = {}

def extract_and_cache(img_path):
    """Extract features and cache them"""
    if img_path not in feature_cache:
        try:
            t, m, _ = extractFeature(img_path)
            feature_cache[img_path] = (t, m)
        except Exception:
            feature_cache[img_path] = None
            console.print(f"[red]Error extracting: {img_path}[/red]")
            return None
    return feature_cache[img_path]


# ============================
# Utility Functions
# ============================

def is_match(distance):
    return distance < THRESHOLD


def is_image_file(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() in VALID_EXTENSIONS


# ============================
# Visualization Functions
# ============================

def print_metrics_table(reg_count, FAR, FRR, ACC):
    table = Table.grid(expand=True)
    table.add_column(justify="center", ratio=1)
    table.add_column(justify="center", ratio=1)

    table.add_row("[bold yellow]FAR[/bold yellow]", f"[red]{FAR:.4f}[/red]")
    table.add_row("[bold yellow]FRR[/bold yellow]", f"[magenta]{FRR:.4f}[/magenta]")
    table.add_row("[bold yellow]Accuracy[/bold yellow]", f"[green]{ACC:.4f}[/green]")

    console.print(Panel(table, title=f"[bold cyan]Enrollment = {reg_count}[/bold cyan]", border_style="bright_blue", box=box.ROUNDED))


def print_confusion_matrix(TP, FN, FP, TN, reg_count):
    table = Table(title=f"Confusion Matrix — Enrollment={reg_count}", box=box.DOUBLE_EDGE, show_lines=True, style="bold white")
    table.add_column("Actual \\ Predicted", justify="center", style="cyan", no_wrap=True)
    table.add_column("Accept", justify="center", style="green")
    table.add_column("Reject", justify="center", style="red")

    table.add_row("[bold green]Genuine[/bold green]", f"[green]{TP}[/green]", f"[red]{FN}[/red]")
    table.add_row("[bold yellow]Impostor[/bold yellow]", f"[yellow]{FP}[/yellow]", f"[bright_black]{TN}[/bright_black]")

    console.print(table)

    total_genuine = TP + FN
    total_impostor = FP + TN
    tpr = (TP / total_genuine * 100) if total_genuine else 0
    tnr = (TN / total_impostor * 100) if total_impostor else 0
    fnr = (FN / total_genuine * 100) if total_genuine else 0
    fpr = (FP / total_impostor * 100) if total_impostor else 0

    console.print(
        f"[bold]TPR:[/bold] {tpr:.2f}%   "
        f"[bold]TNR:[/bold] {tnr:.2f}%   "
        f"[bold]FAR:[/bold] {fpr:.2f}%   "
        f"[bold]FRR:[/bold] {fnr:.2f}%"
    )


def print_accuracy_summary(results):
    best_reg_count = max(results.keys(), key=lambda k: results[k]["Accuracy"])

    summary = Table(title="Final Performance Summary", box=box.SIMPLE_HEAVY, show_lines=True)
    summary.add_column("Enrollment", justify="center", style="cyan")
    summary.add_column("Accuracy", justify="center", style="green")
    summary.add_column("FAR", justify="center", style="red")
    summary.add_column("FRR", justify="center", style="magenta")

    for reg_count in sorted(results.keys()):
        row_style = "bold bright_white on blue" if reg_count == best_reg_count else ""
        summary.add_row(
            f"[bold]{reg_count}[/bold]",
            f"[green]{results[reg_count]['Accuracy']:.4f}[/green]",
            f"[red]{results[reg_count]['FAR']:.4f}[/red]",
            f"[magenta]{results[reg_count]['FRR']:.4f}[/magenta]",
            style=row_style
        )

    console.print(Panel(summary, border_style="bright_magenta", title="[bold yellow]Evaluation Summary[/bold yellow]"))


def plot_accuracy_heatmap(results, output_path="accuracy_heatmap.png"):
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        console.print("[yellow]Matplotlib or seaborn is not installed. Heatmap export skipped.[/yellow]")
        return

    metric_names = ["Accuracy", "FAR", "FRR"]
    reg_counts = sorted(results.keys())
    heatmap_data = np.array([
        [results[reg][metric] for metric in metric_names]
        for reg in reg_counts
    ])

    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 0.8 * len(reg_counts) + 2))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".4f",
        cmap="viridis",
        linewidths=0.8,
        linecolor="white",
        xticklabels=metric_names,
        yticklabels=[str(reg) for reg in reg_counts],
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    ax.set_title("Accuracy Evaluation Heatmap", fontsize=14, weight="bold")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Enrollment Count")
    fig.tight_layout()

    try:
        fig.savefig(output_path, dpi=200)
        console.print(Panel(f"[bold green]Heatmap saved to:[/bold green] {output_path}", border_style="green", title="[bold cyan]Heatmap Export[/bold cyan]"))
    except Exception as exc:
        console.print(f"[red]Failed to save heatmap:[/red] {exc}")
    finally:
        plt.close(fig)


# ============================
# Core Evaluation Logic
# ============================

def evaluate_user(user_id, enrollment_imgs, test_imgs, impostor_users_list, gen_num, imp_num):
    false_reject = 0
    false_accept = 0
    genuine_total = 0
    impostor_total = 0

    enrollment_templates = []
    for img in enrollment_imgs:
        if not is_image_file(img):
            continue
        features = extract_and_cache(img)
        if features:
            enrollment_templates.append(features)

    if not enrollment_templates:
        return 0, 0, 0, 0

    # Genuine Matching
    for test_img in test_imgs:
        if not is_image_file(test_img):
            continue

        test_features = extract_and_cache(test_img)
        if not test_features:
            continue

        test_template, test_mask = test_features
        distances = [
            HammingDistance(test_template, test_mask, et, em)
            for et, em in enrollment_templates
        ]

        min_distance = min(distances)
        genuine_total += 1

        if not is_match(min_distance):
            false_reject += 1

    # Impostor Matching
    for other_user_id, impostor_imgs in impostor_users_list:
        for test_img in impostor_imgs:
            if not is_image_file(test_img):
                continue

            test_features = extract_and_cache(test_img)
            if not test_features:
                continue

            test_template, test_mask = test_features
            distances = [
                HammingDistance(test_template, test_mask, et, em)
                for et, em in enrollment_templates
            ]

            min_distance = min(distances)
            impostor_total += 1

            if is_match(min_distance):
                false_accept += 1

    gen_num[0] += genuine_total
    imp_num[0] += impostor_total

    return false_reject, false_accept, genuine_total, impostor_total


# ============================
# Main Evaluation Function
# ============================

def evaluate_system(dataset_path):
    console.print(f"[bold cyan]Loading dataset from: {dataset_path}[/bold cyan]")

    all_users_data = {}

    for user_dir in sorted(os.listdir(dataset_path)):
        user_path = os.path.join(dataset_path, user_dir)

        if not os.path.isdir(user_path):
            continue

        images = [
            os.path.join(user_path, f)
            for f in os.listdir(user_path)
            if is_image_file(os.path.join(user_path, f))
        ]

        if len(images) >= 6:
            all_users_data[user_dir] = images

    console.print(f"[green]Loaded {len(all_users_data)} users[/green]\n")

    results = {}
    users_list = list(all_users_data.items())

    for reg_count in range(1, 6):
        console.rule(f"[yellow]Enrollment Images = {reg_count}[/yellow]")

        start_time = time.time()
        total_fr = total_fa = total_gen = total_imp = 0

        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=None, style="yellow", complete_style="bright_yellow"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing users...", total=len(users_list))

            for user_id, images in users_list:
                if len(images) <= reg_count:
                    progress.update(task, advance=1)
                    continue

                shuffled = images.copy()
                random.shuffle(shuffled)

                enrollment_imgs = shuffled[:reg_count]
                test_imgs = shuffled[reg_count:]

                other_users = [u for u in users_list if u[0] != user_id]
                impostor_sample = random.sample(
                    other_users,
                    min(IMPOSTOR_USERS_SAMPLE, len(other_users))
                )

                impostor_data = [
                    (oid, imgs[reg_count:])
                    for oid, imgs in impostor_sample
                    if len(imgs) > reg_count
                ]

                gen_num = [0]
                imp_num = [0]

                fr, fa, gen, imp = evaluate_user(
                    user_id,
                    enrollment_imgs,
                    test_imgs,
                    impostor_data,
                    gen_num,
                    imp_num
                )

                total_fr += fr
                total_fa += fa
                total_gen += gen
                total_imp += imp

                progress.update(task, advance=1)

        elapsed = time.time() - start_time

        FAR = total_fa / total_imp if total_imp else 0
        FRR = total_fr / total_gen if total_gen else 0
        ACC = 1 - ((total_fa + total_fr) / (total_gen + total_imp)) if (total_gen + total_imp) else 0

        TP = total_gen - total_fr
        FN = total_fr
        FP = total_fa
        TN = total_imp - total_fa

        results[reg_count] = {
            "FAR": FAR,
            "FRR": FRR,
            "Accuracy": ACC,
            "TP": TP,
            "FN": FN,
            "FP": FP,
            "TN": TN
        }

        console.print(f"[bold green]Completed in {elapsed:.2f}s[/bold green]")

        print_metrics_table(reg_count, FAR, FRR, ACC)
        print_confusion_matrix(TP, FN, FP, TN, reg_count)

    return results


# ============================
# Run Script
# ============================

if __name__ == "__main__":
    results = evaluate_system("CASIA1")

    console.rule("[bold magenta]FINAL SUMMARY[/bold magenta]")

    for k, v in results.items():
        print_metrics_table(k, v["FAR"], v["FRR"], v["Accuracy"])

    print_accuracy_summary(results)
    plot_accuracy_heatmap(results)