"""
Name: Rinji Le
Student ID: 13344552
Course: Afstudeerproject Bachelor Informatica
Date: TODO

Description:
TODO
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from tqdm import tqdm

classifiers = [
    "LogisticRegression",
    "GaussianNB",
    "BernoulliNB",
    "MultinomialNB",
    "KNeighborsClassifier",
    "SVC",
    "MLPClassifier",
    "DecisionTreeClassifier",
    "RandomForestClassifier"
]

# The model names are used for the plots
model_names = {
    "LogisticRegression": "Logistic Regression",
    "GaussianNB": "Gaussian Naive Bayes",
    "BernoulliNB": "Bernoulli Naive Bayes",
    "MultinomialNB": "Multinomial Naive Bayes",
    "KNeighborsClassifier": "K-Nearest Neighbors",
    "SVC": "Support Vector Machine",
    "MLPClassifier": "Neural Network",
    "DecisionTreeClassifier": "Decision Tree",
    "RandomForestClassifier": "Random Forest",

    "LinearRegression": " Linear Regression",
    "KNeighborsRegressor": " K-Nearest Neighbors",
    "SVR": " Support Vector Machine",
    "MLPRegressor": " Neural Network",
    "DecisionTreeRegressor": " Decision Tree",
    "RandomForestRegressor": " Random Forest"
}


def plot_bars(data, filename, n, model_type="all"):
    if model_type == "classification":
        data = data[data["type"] == model_type]
        title = "Nauwkeurigheid van verschillende classificators"
    elif model_type == "regression":
        data = data[data["type"] == model_type]
        title = "Nauwkeurigheid van verschillende regressors"
    else:
        title = "Nauwkeurigheid van verschillende modellen"

    data = data.sort_values(by="accuracy", ascending=True)
    colors = ["royalblue" if row["type"] == "classification" else "limegreen"
              for (_, row) in data.iterrows()]

    bars = plt.barh([model_names[model] for model in data["model"]],
                    data["accuracy"], color=colors, edgecolor="black",
                    alpha=0.8)

    # If the accuracy is lower than 5%, place the label on the right side of
    # the bar, otherwise place it in the middle
    for bar in bars:
        width = bar.get_width()

        if width < 6:
            plt.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                     f"{width:.2f}%", va="center")
        else:
            plt.text(width / 2, bar.get_y() + bar.get_height() / 2,
                     f"{width:.2f}%", va="center", ha="center")

    plt.title(title)
    plt.xlabel("Nauwkeurigheid (%)")

    # Add legend if both classifiers and regressors are present in the data
    if model_type == "all" and len(data["type"].unique()) == 2:
        labels = ["Classificator", "Regressor"]
        colors = ["royalblue", "limegreen"]
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i], alpha=0.8)
                   for i in range(len(labels))]
        plt.legend(handles, labels, loc="best")

    plt.tight_layout()
    plt.savefig(f"plots/n{n}/{filename}_{model_type}.png", dpi=1000)
    plt.clf()  # Clear the figure


def plot_learning_curve(data, model, n):
    # Multiply the data by 100 to get the accuracy in percentages
    if model in classifiers:
        data = data.apply(lambda x: x * 100 if x.name != "train_size" else x)

    plt.plot(data["train_size"], data["train_mean"], label="Train-score",
             marker="o", color="royalblue")
    plt.fill_between(data["train_size"], data["train_ci_lower"],
                     data["train_ci_upper"], label="95% CI (train)",
                     alpha=0.2, color="royalblue")
    plt.plot(data["train_size"], data["validation_mean"],
             label="Validatie-score", marker="o", color="limegreen")
    plt.fill_between(data["train_size"], data["validation_ci_lower"],
                     data["validation_ci_upper"], label="95% CI (validatie)",
                     alpha=0.2, color="limegreen")

    plt.title(f"{model_names[model]}: leercurve met 5-voudige kruisvalidatie")
    plt.xlabel("Trainset grootte")

    if model in classifiers:
        plt.ylabel("Nauwkeurigheid (%)")
    else:
        plt.ylabel("Gemiddelde absolute fout (negatie)")

    plt.legend(loc="best")
    plt.savefig(f"plots/n{n}/learning_curve_{model}{n}.png", dpi=1000)
    plt.clf()  # Clear the figure


def main():
    if len(sys.argv) < 2:
        print("Usage: python plot.py --bar <n> <file>")
        print("       python plot.py --lc <n> [file]")
        sys.exit(1)

    if sys.argv[1] == "--help":
        print("Usage: python plot.py --bar <n> <file>")
        print("       python plot.py --lc <n> [file]")
        sys.exit(0)
    elif sys.argv[1] == "--bar":
        if len(sys.argv) < 4:
            print("Usage: python plot.py --bar <n> <file>")
            sys.exit(1)
        else:
            data = pd.read_csv(sys.argv[3])

            # File name without the dictionary and extension
            filename = sys.argv[3].split("/")[2].split(".")[0]
            n = int(sys.argv[2])

            plot_bars(data, filename, n)
            plot_bars(data, filename, n, model_type="classification")
            plot_bars(data, filename, n, model_type="regression")
    elif sys.argv[1] == "--lc":
        if len(sys.argv) < 3:
            print("Usage: python plot.py --lc <n> [file]")
            sys.exit(1)

        n = int(sys.argv[2])

        if len(sys.argv) > 3:
            file = sys.argv[3]
            files = [file.split("/")[2]]
        else:
            files = os.listdir(f"results/n{n}")
            files = [file for file in files if file[:14] == "learning_curve"]

        for file in tqdm(files, desc="Plotting learning curves"):
            model = file.split("_")[-1].split(".")[0]
            # Remove the number at the end of the file name
            model = model[:-1] if model[-1].isdigit() else model
            model = model[:-1] if model[-1].isdigit() else model

            data = pd.read_csv(f"results/n{n}/{file}")
            plot_learning_curve(data, model, n)


if __name__ == "__main__":
    main()
