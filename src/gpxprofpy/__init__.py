"""
## GPX profile plotter

Contains tool for plotting a GPX elevation profile.

Import plot_gpx_profile function to use
"""

from . import profiler as prf


def plot_gpx_profile(
    filename: str,
    plot_slope: bool = False,
    plot_points: bool = False,
    save_fig: bool = False,
) -> None:
    """
    Parameters
    ----------

    filename : str
        GPX file name.

    plot_slope: bool, optional
        Plot slope segments (default: False). If activated, plot segments that are longerr than
        variable SEUIL defined in .params. Segments colors are choosen accordingly to their
        mean slope, and colors are also defined in .params.

    plot_points: bool, optional
        Plot remarquables points (default: False). If activated, module tries to open a CSV file
        with the same name as the main GPX file. Remarquable points are red as
        (distance, label, has_water). Points are then added on the profile, with different
        styling for start and finish points. Colors are also defined in .params.

    save_fig: bool, optional
        Save plot as png file (default: False). If activated, plot is saved to a png
        file with the same name as the main GPX file.


    Examples
    ----------
    >>> plot_gpx_profile("data/RAF_500.gpx")
        Plots elevation profile only

    >>> plot_gpx_profile("data/RAF_500.gpx", True, True, True)
        Plots elevation profile, slope segments, remarquables points and saves a png file

    >>> plot_gpx_profile("data/RAF_500.gpx", save_fig=True)
        Plots elevation profile and saves a png file
    """

    gpx_file = prf.GPXFile(filename)
    gpx_profile = gpx_file.profile()
    gpx_profile.plot(plot_slope, plot_points, save_fig)
