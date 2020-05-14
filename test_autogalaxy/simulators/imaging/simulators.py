import autolens as al

from test_autolens.simulators.imaging import instrument_util


def simulate__galaxy_x1__dev_vaucouleurs(instrument):

    data_label = "galaxy_x1__dev_vaucouleurs"

    # This lens-only system has a Dev Vaucouleurs spheroid / bulge.

    lens_galaxy = al.Galaxy(
        redshift=0.5,
        bulge=al.lp.EllipticalDevVaucouleurs(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.1,
            effective_radius=1.0,
        ),
    )

    instrument_util.simulate_imaging_from_instrument(
        data_label=data_label,
        instrument=instrument,
        galaxies=[lens_galaxy, al.Galaxy(redshift=1.0)],
    )


def simulate__galaxy_x1__bulge_disk(instrument):

    data_label = "galaxy_x1__bulge_disk"

    # This source-only system has a Dev Vaucouleurs spheroid / bulge and surrounding Exponential envelope

    lens_galaxy = al.Galaxy(
        redshift=0.5,
        bulge=al.lp.EllipticalDevVaucouleurs(
            centre=(0.0, 0.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.1,
            effective_radius=1.0,
        ),
        envelope=al.lp.EllipticalExponential(
            centre=(0.0, 0.0),
            axis_ratio=0.7,
            phi=60.0,
            intensity=1.0,
            effective_radius=2.0,
        ),
    )

    instrument_util.simulate_imaging_from_instrument(
        data_label=data_label,
        instrument=instrument,
        galaxies=[lens_galaxy, al.Galaxy(redshift=1.0)],
    )


def simulate__galaxy_x2__sersics(instrument):

    data_label = "galaxy_x2__sersics"

    # This source-only system has two Sersic bulges separated by 2.0"

    lens_galaxy_0 = al.Galaxy(
        redshift=0.5,
        bulge=al.lp.EllipticalSersic(
            centre=(-1.0, -1.0),
            axis_ratio=0.8,
            phi=0.0,
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=3.0,
        ),
    )

    lens_galaxy_1 = al.Galaxy(
        redshift=0.5,
        bulge=al.lp.EllipticalSersic(
            centre=(1.0, 1.0),
            axis_ratio=0.8,
            phi=0.0,
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=3.0,
        ),
    )

    instrument_util.simulate_imaging_from_instrument(
        data_label=data_label,
        instrument=instrument,
        galaxies=[lens_galaxy_0, lens_galaxy_1, al.Galaxy(redshift=1.0)],
    )


def simulate__galaxy_x1__dev_vaucouleurs__offset_centre(instrument):

    data_label = "galaxy_x1__dev_vaucouleurs__offset_centre"

    # This lens-only system has a Dev Vaucouleurs spheroid / bulge.

    lens_galaxy = al.Galaxy(
        redshift=0.5,
        bulge=al.lp.EllipticalDevVaucouleurs(
            centre=(2.0, 2.0),
            axis_ratio=0.9,
            phi=45.0,
            intensity=0.1,
            effective_radius=1.0,
        ),
    )

    instrument_util.simulate_imaging_from_instrument(
        data_label=data_label,
        instrument=instrument,
        galaxies=[lens_galaxy, al.Galaxy(redshift=1.0)],
    )
