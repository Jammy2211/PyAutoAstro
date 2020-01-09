import autoarray as aa
import matplotlib

backend = aa.conf.get_matplotlib_backend()
matplotlib.use(backend)
from matplotlib import pyplot as plt

from autoarray.plotters import array_plotters
from autoastro.plots import profile_plots, lens_plotter_util


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def profile_image(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the image (e.g. the datas) of a galaxy, on a grid of (y,x) coordinates.

    Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    galaxy : model.galaxy.aast.Galaxy
        The galaxy whose image are plotted.
    grid : ndarray or datas.arrays.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
    """
    image = galaxy.profile_image_from_grid(grid=grid)

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(array=image, mask=mask, points=positions, lines=lines)


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def convergence(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the convergence of a galaxy, on a grid of (y,x) coordinates.

    Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    galaxy : model.galaxy.aast.Galaxy
        The galaxy whose convergence is plotted.
    grid : ndarray or datas.arrays.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
    """
    convergence = galaxy.convergence_from_grid(grid=grid)

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(
        array=convergence, mask=mask, points=positions, lines=lines
    )


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def potential(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the potential of a galaxy, on a grid of (y,x) coordinates.

     Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

     Parameters
     -----------
    galaxy : model.galaxy.aast.Galaxy
         The galaxy whose potential is plotted.
    grid : ndarray or datas.arrays.grid_stacks.Grid
         The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
     """
    potential = galaxy.potential_from_grid(grid=grid)

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(array=potential, mask=mask, points=positions, lines=lines)


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def deflections_y(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the y component of the deflection angles of a galaxy, on a grid of (y,x) coordinates.

    Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    galaxy : model.galaxy.aast.Galaxy
        The galaxy whose y deflecton angles are plotted.
    grid : ndarray or datas.arrays.grid_stacks.Grid
        The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
    """
    deflections = galaxy.deflections_from_grid(grid=grid)
    deflections_y = grid.mapping.array_stored_1d_from_sub_array_1d(
        sub_array_1d=deflections[:, 0]
    )

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(
        array=deflections_y, mask=mask, points=positions, lines=lines
    )


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def deflections_x(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the x component of the deflection angles of a galaxy, on a grid of (y,x) coordinates.

     Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

     Parameters
     -----------
    galaxy : model.galaxy.aast.Galaxy
         The galaxy whose x deflecton angles are plotted.
     grid : ndarray or datas.arrays.grid_stacks.Grid
         The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
     """
    deflections = galaxy.deflections_from_grid(grid=grid)
    deflections_x = grid.mapping.array_stored_1d_from_sub_array_1d(
        sub_array_1d=deflections[:, 1]
    )

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(
        array=deflections_x, mask=mask, points=positions, lines=lines
    )


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def magnification(
    galaxy,
    grid,
    mask=None,
    positions=None,
    include_critical_curves=False,
    include_caustics=False,
    array_plotter=array_plotters.ArrayPlotter(),
):
    """Plot the magnification of a galaxy, on a grid of (y,x) coordinates.

     Set *autoastro.datas.arrays.plotters.array_plotters* for a description of all innput parameters not described below.

     Parameters
     -----------
    galaxy : model.galaxy.aast.Galaxy
         The galaxy whose magnification is plotted.
    grid : ndarray or datas.arrays.grid_stacks.Grid
         The (y,x) coordinates of the grid, in an arrays of shape (total_coordinates, 2)
     """
    magnification = galaxy.magnification_from_grid(grid=grid)

    lines = lens_plotter_util.critical_curves_and_caustics_from_lensing_object(
        obj=galaxy,
        include_critical_curves=include_critical_curves,
        include_caustics=include_caustics,
    )

    array_plotter.plot_array(
        array=magnification, mask=mask, points=positions, lines=lines
    )


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def profile_image_subplot(
    galaxy, grid, mask=None, positions=None, array_plotter=array_plotters.ArrayPlotter()
):

    total_light_profiles = len(galaxy.light_profiles)

    array_plotter = array_plotter.plotter_as_sub_plotter()

    rows, columns, figsize_tool = array_plotter.get_subplot_rows_columns_figsize(
        number_subplots=total_light_profiles
    )

    if array_plotter.figsize is None:
        figsize = figsize_tool
    else:
        figsize = array_plotter.figsize

    plt.figure(figsize=figsize)

    for i, light_profile in enumerate(galaxy.light_profiles):

        plt.subplot(rows, columns, i + 1)

        profile_plots.image(
            light_profile=light_profile,
            mask=mask,
            positions=positions,
            grid=grid,
            array_plotter=array_plotter,
        )

    array_plotter.output_subplot_array()
    plt.close()


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def convergence_subplot(
    galaxy, grid, mask=None, positions=None, array_plotter=array_plotters.ArrayPlotter()
):

    total_mass_profiles = len(galaxy.mass_profiles)

    array_plotter = array_plotter.plotter_as_sub_plotter()

    rows, columns, figsize_tool = array_plotter.get_subplot_rows_columns_figsize(
        number_subplots=total_mass_profiles
    )

    if array_plotter.figsize is None:
        figsize = figsize_tool
    else:
        figsize = array_plotter.figsize

    plt.figure(figsize=figsize)

    for i, mass_profile in enumerate(galaxy.mass_profiles):

        plt.subplot(rows, columns, i + 1)

        profile_plots.convergence(
            mass_profile=mass_profile,
            grid=grid,
            mask=mask,
            positions=positions,
            array_plotter=array_plotter,
        )

    array_plotter.output_subplot_array()
    plt.close()


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def potential_subplot(
    galaxy, grid, mask=None, positions=None, array_plotter=array_plotters.ArrayPlotter()
):

    total_mass_profiles = len(galaxy.mass_profiles)
    array_plotter = array_plotter.plotter_as_sub_plotter()

    rows, columns, figsize_tool = array_plotter.get_subplot_rows_columns_figsize(
        number_subplots=total_mass_profiles
    )

    if array_plotter.figsize is None:
        figsize = figsize_tool
    else:
        figsize = array_plotter.figsize

    plt.figure(figsize=figsize)

    for i, mass_profile in enumerate(galaxy.mass_profiles):

        plt.subplot(rows, columns, i + 1)

        profile_plots.potential(
            mass_profile=mass_profile,
            grid=grid,
            mask=mask,
            positions=positions,
            array_plotter=array_plotter,
        )

    array_plotter.output_subplot_array()
    plt.close()


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def deflections_y_subplot(
    galaxy, grid, mask=None, positions=None, array_plotter=array_plotters.ArrayPlotter()
):

    total_mass_profiles = len(galaxy.mass_profiles)
    array_plotter = array_plotter.plotter_as_sub_plotter()

    rows, columns, figsize_tool = array_plotter.get_subplot_rows_columns_figsize(
        number_subplots=total_mass_profiles
    )

    if array_plotter.figsize is None:
        figsize = figsize_tool
    else:
        figsize = array_plotter.figsize

    plt.figure(figsize=figsize)

    for i, mass_profile in enumerate(galaxy.mass_profiles):

        plt.subplot(rows, columns, i + 1)

        profile_plots.deflections_y(
            mass_profile=mass_profile,
            grid=grid,
            mask=mask,
            positions=positions,
            array_plotter=array_plotter,
        )

    array_plotter.output_subplot_array()
    plt.close()


@lens_plotter_util.set_includes
@lens_plotter_util.set_labels_and_unit_conversion
def deflections_x_subplot(
    galaxy, grid, mask=None, positions=None, array_plotter=array_plotters.ArrayPlotter()
):

    total_mass_profiles = len(galaxy.mass_profiles)
    array_plotter = array_plotter.plotter_as_sub_plotter()

    rows, columns, figsize_tool = array_plotter.get_subplot_rows_columns_figsize(
        number_subplots=total_mass_profiles
    )

    if array_plotter.figsize is None:
        figsize = figsize_tool
    else:
        figsize = array_plotter.figsize

    plt.figure(figsize=figsize)

    for i, mass_profile in enumerate(galaxy.mass_profiles):

        plt.subplot(rows, columns, i + 1)

        profile_plots.deflections_x(
            mass_profile=mass_profile,
            grid=grid,
            mask=mask,
            positions=positions,
            array_plotter=array_plotter,
        )

    array_plotter.output_subplot_array()
    plt.close()