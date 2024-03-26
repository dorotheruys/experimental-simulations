import json
import matplotlib.pyplot as plt
import numpy as np


class PlotData:
    def __init__(self, time_label: str, time_unit: str, data_label: str, data_unit: str):
        """
        :param time_label: Label that appears on the x-axis of the plot
        :param data_label: Label that appears on the y-axis of the plot
        Class that is used to collect the data before plotting
        """
        self.tags: list[str] = []
        self.time: dict = {}  # Time with label that will appear in the legend
        self.data: dict = {}  # Data with label that will appear in the legend
        self.time_label: str = time_label
        self.time_unit: str = time_unit
        self.data_label: str = data_label
        self.data_unit: str = data_unit

    def append(self, data: np.array, time: np.array, label: str):
        """
        :param data: Numpy array with all the y-values
        :param time: Numpy array with all the x-values
        :param label: String with the name of the current measurement
        :return: self
        """
        self.tags.append(label)
        self.data[label] = data
        self.time[label] = time
        return self


class StylePlot:
    def __init__(self):
        self.colours = ["#000000"]
        self.grid = False
        self.legend = True
        self.xlim = [None, None]
        self.ylim = [None, None]

    def import_style(self, style_name: str, path: str = "./styles/plot_styles.json"):
        print("Importing plotting style")
        # Get the plot_styles json file from path
        try:
            with open(path, 'rb') as file:
                styles = json.load(file)
        except FileNotFoundError:
            print(f"\tStyle file not found in directory: '{path}'\nResorting to standard style")
            return -1
        # Get the correct style from the plot_styles json
        try:
            style = styles[style_name]
        except KeyError:
            print(f"\tNo style was found with style_name: '{style_name}'\nResorting to standard style")
            return -1
        # Change standard values to that of the imported style
        for key, value in style.items():
            if key in self.__dict__:
                self.__dict__[key] = value
            else:
                print(f"\tDid not find the attribute '{key}' in the StylePlot class, so it was not added")
        print("Finished importing plotting style")

    def plot(self, plot_data: PlotData, save: str = ""):
        for i, tag in enumerate(plot_data.tags):
            plt.plot(plot_data.time[tag], plot_data.data[tag], label=tag, color=self.colours[i])

        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        if self.grid:
            plt.grid()
        if self.legend:
            plt.legend()
        plt.xlabel(f"{plot_data.time_label} [{plot_data.time_unit}]")
        plt.ylabel(f"{plot_data.data_label} [{plot_data.data_unit}]")

        if save:
            plt.savefig(f"./data_files/plots/{save}")
        else:
            plt.show()


if __name__ == "__main__":
    style_plot = StylePlot()
    style_plot.import_style("tudelft_housestyle")

    data = PlotData("q", "deg/s", "Time", "s")
    data.append(np.array([2, 4, 5]), np.array([2, 3, 4]), "Simplified")
    style_plot.plot(data)
