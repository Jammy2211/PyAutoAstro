from __future__ import division, print_function

import math
import numpy as np
import pytest
import scipy.special

import autofit as af
import automodel as am
from test_automodel.mock import mock_cosmology


@pytest.fixture(autouse=True)
def reset_config():
    """
    Use configuration from the default path. You may want to change this to set a specific path.
    """
    af.conf.instance = af.conf.default


grid = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


class TestGaussian:
    def test__constructor_and_units(self):
        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(1.0, 2.0), axis_ratio=0.5, phi=45.0, intensity=1.0, sigma=0.1
        )

        assert gaussian.centre == (1.0, 2.0)
        assert isinstance(gaussian.centre[0], am.Length)
        assert isinstance(gaussian.centre[1], am.Length)
        assert gaussian.centre[0].unit == "arcsec"
        assert gaussian.centre[1].unit == "arcsec"

        assert gaussian.axis_ratio == 0.5
        assert isinstance(gaussian.axis_ratio, float)

        assert gaussian.phi == 45.0
        assert isinstance(gaussian.phi, float)

        assert gaussian.intensity == 1.0
        assert isinstance(gaussian.intensity, am.Luminosity)
        assert gaussian.intensity.unit == "eps"

        assert gaussian.sigma == 0.1
        assert isinstance(gaussian.sigma, am.Length)
        assert gaussian.sigma.unit_length == "arcsec"

        gaussian = am.light_profiles.SphericalGaussian(
            centre=(1.0, 2.0), intensity=1.0, sigma=0.1
        )

        assert gaussian.centre == (1.0, 2.0)
        assert isinstance(gaussian.centre[0], am.Length)
        assert isinstance(gaussian.centre[1], am.Length)
        assert gaussian.centre[0].unit == "arcsec"
        assert gaussian.centre[1].unit == "arcsec"

        assert gaussian.axis_ratio == 1.0
        assert isinstance(gaussian.axis_ratio, float)

        assert gaussian.phi == 0.0
        assert isinstance(gaussian.phi, float)

        assert gaussian.intensity == 1.0
        assert isinstance(gaussian.intensity, am.Luminosity)
        assert gaussian.intensity.unit == "eps"

        assert gaussian.sigma == 0.1
        assert isinstance(gaussian.sigma, am.Length)
        assert gaussian.sigma.unit_length == "arcsec"

    def test__intensity_as_radius__correct_value(self):
        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=1.0
        )
        assert gaussian.profile_image_from_grid_radii(grid_radii=1.0) == pytest.approx(
            0.24197, 1e-2
        )

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=2.0, sigma=1.0
        )
        assert gaussian.profile_image_from_grid_radii(grid_radii=1.0) == pytest.approx(
            2.0 * 0.24197, 1e-2
        )

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=2.0
        )
        assert gaussian.profile_image_from_grid_radii(grid_radii=1.0) == pytest.approx(
            0.1760, 1e-2
        )

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=2.0
        )
        assert gaussian.profile_image_from_grid_radii(grid_radii=3.0) == pytest.approx(
            0.0647, 1e-2
        )

    def test__intensity_from_grid__same_values_as_above(self):
        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=1.0
        )
        assert gaussian.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(0.24197, 1e-2)

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=2.0, sigma=1.0
        )

        assert gaussian.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(2.0 * 0.24197, 1e-2)

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=2.0
        )

        assert gaussian.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(0.1760, 1e-2)

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=2.0
        )

        assert gaussian.profile_image_from_grid(
            grid=np.array([[0.0, 3.0]])
        ) == pytest.approx(0.0647, 1e-2)

    def test__intensity_from_grid__change_geometry(self):
        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(1.0, 1.0), axis_ratio=1.0, phi=0.0, intensity=1.0, sigma=1.0
        )
        assert gaussian.profile_image_from_grid(
            grid=np.array([[1.0, 0.0]])
        ) == pytest.approx(0.24197, 1e-2)

        gaussian = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=0.0, intensity=1.0, sigma=1.0
        )
        assert gaussian.profile_image_from_grid(
            grid=np.array([[1.0, 0.0]])
        ) == pytest.approx(0.05399, 1e-2)

        gaussian_0 = am.light_profiles.EllipticalGaussian(
            centre=(-3.0, -0.0), axis_ratio=0.5, phi=0.0, intensity=1.0, sigma=1.0
        )

        gaussian_1 = am.light_profiles.EllipticalGaussian(
            centre=(3.0, 0.0), axis_ratio=0.5, phi=0.0, intensity=1.0, sigma=1.0
        )

        assert gaussian_0.profile_image_from_grid(
            grid=np.array([[0.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
        ) == pytest.approx(
            gaussian_1.profile_image_from_grid(
                grid=np.array([[0.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
            ),
            1e-4,
        )

        gaussian_0 = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=180.0, intensity=1.0, sigma=1.0
        )

        gaussian_1 = am.light_profiles.EllipticalGaussian(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=0.0, intensity=1.0, sigma=1.0
        )

        assert gaussian_0.profile_image_from_grid(
            grid=np.array([[0.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
        ) == pytest.approx(
            gaussian_1.profile_image_from_grid(
                grid=np.array([[0.0, 0.0], [0.0, -1.0], [0.0, 1.0]])
            ),
            1e-4,
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = am.light_profiles.EllipticalGaussian(
            axis_ratio=1.0, phi=0.0, intensity=3.0, sigma=2.0
        )
        spherical = am.light_profiles.SphericalGaussian(intensity=3.0, sigma=2.0)

        assert (
            ellipticam.profile_image_from_grid(grid=grid)
            == sphericam.profile_image_from_grid(grid=grid)
        ).all()

    def test__reshape_results(self):
        grid = aa.grid.uniform(
            shape_2d=(2, 2), pixel_scales=1.0, sub_size=1
        )

        gaussian = am.light_profiles.EllipticalGaussian()

        image = gaussian.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)

        gaussian = am.light_profiles.SphericalGaussian()

        image = gaussian.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)


class TestSersic:
    def test__constructor_and_units(self):
        sersic = am.light_profiles.EllipticalSersic(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            intensity=1.0,
            effective_radius=0.6,
            sersic_index=4.0,
        )

        assert sersic.centre == (1.0, 2.0)
        assert isinstance(sersic.centre[0], am.Length)
        assert isinstance(sersic.centre[1], am.Length)
        assert sersic.centre[0].unit == "arcsec"
        assert sersic.centre[1].unit == "arcsec"

        assert sersic.axis_ratio == 0.5
        assert isinstance(sersic.axis_ratio, float)

        assert sersic.phi == 45.0
        assert isinstance(sersic.phi, float)

        assert sersic.intensity == 1.0
        assert isinstance(sersic.intensity, am.Luminosity)
        assert sersic.intensity.unit == "eps"

        assert sersic.effective_radius == 0.6
        assert isinstance(sersic.effective_radius, am.Length)
        assert sersic.effective_radius.unit_length == "arcsec"

        assert sersic.sersic_index == 4.0
        assert isinstance(sersic.sersic_index, float)

        assert sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert sersic.elliptical_effective_radius == 0.6 / np.sqrt(0.5)

        sersic = am.light_profiles.SphericalSersic(
            centre=(1.0, 2.0), intensity=1.0, effective_radius=0.6, sersic_index=4.0
        )

        assert sersic.centre == (1.0, 2.0)
        assert isinstance(sersic.centre[0], am.Length)
        assert isinstance(sersic.centre[1], am.Length)
        assert sersic.centre[0].unit == "arcsec"
        assert sersic.centre[1].unit == "arcsec"

        assert sersic.axis_ratio == 1.0
        assert isinstance(sersic.axis_ratio, float)

        assert sersic.phi == 0.0
        assert isinstance(sersic.phi, float)

        assert sersic.intensity == 1.0
        assert isinstance(sersic.intensity, am.Luminosity)
        assert sersic.intensity.unit == "eps"

        assert sersic.effective_radius == 0.6
        assert isinstance(sersic.effective_radius, am.Length)
        assert sersic.effective_radius.unit_length == "arcsec"

        assert sersic.sersic_index == 4.0
        assert isinstance(sersic.sersic_index, float)

        assert sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert sersic.elliptical_effective_radius == 0.6

    def test__intensity_at_radius__correct_value(self):
        sersic = am.light_profiles.EllipticalSersic(
            axis_ratio=1.0,
            phi=0.0,
            intensity=1.0,
            effective_radius=0.6,
            sersic_index=4.0,
        )
        assert sersic.profile_image_from_grid_radii(grid_radii=1.0) == pytest.approx(
            0.351797, 1e-3
        )

        sersic = am.light_profiles.EllipticalSersic(
            axis_ratio=1.0,
            phi=0.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )
        # 3.0 * exp(-3.67206544592 * (1,5/2.0) ** (1.0 / 2.0)) - 1) = 0.351797
        assert sersic.profile_image_from_grid_radii(grid_radii=1.5) == pytest.approx(
            4.90657319276, 1e-3
        )

    def test__intensity_from_grid__correct_values(self):
        sersic = am.light_profiles.EllipticalSersic(
            axis_ratio=0.5,
            phi=0.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )
        assert sersic.profile_image_from_grid(
            grid=np.array([[1.0, 0.0]])
        ) == pytest.approx(5.38066670129, 1e-3)

    def test__intensity_from_grid__change_geometry(self):
        sersic_0 = am.light_profiles.EllipticalSersic(
            axis_ratio=0.5,
            phi=0.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )

        sersic_1 = am.light_profiles.EllipticalSersic(
            axis_ratio=0.5,
            phi=90.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )

        assert sersic_0.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == sersic_1.profile_image_from_grid(grid=np.array([[1.0, 0.0]]))

    def test__spherical_and_elliptical_match(self):
        elliptical = am.light_profiles.EllipticalSersic(
            axis_ratio=1.0,
            phi=0.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )

        spherical = am.light_profiles.SphericalSersic(
            intensity=3.0, effective_radius=2.0, sersic_index=2.0
        )

        assert (
            ellipticam.profile_image_from_grid(grid=grid)
            == sphericam.profile_image_from_grid(grid=grid)
        ).all()

    def test__summarize_in_units(self):
        sersic = am.light_profiles.SphericalSersic(
            intensity=3.0, effective_radius=2.0, sersic_index=2.0
        )

        summary_text = sersic.summarize_in_units(
            radii=[am.Length(10.0), am.Length(500.0)],
            prefix="sersic_",
            unit_length="arcsec",
            unit_luminosity="eps",
            whitespace=50,
        )

        i = 0

        assert summary_text[i] == "Light Profile = SphericalSersic\n"
        i += 1
        assert (
            summary_text[i]
            == "sersic_luminosity_within_10.00_arcsec             1.8854e+02 eps"
        )
        i += 1
        assert (
            summary_text[i]
            == "sersic_luminosity_within_500.00_arcsec            1.9573e+02 eps"
        )
        i += 1

    def test__reshape_decorators(self):
        grid = aa.grid.uniform(
            shape_2d=(2, 2), pixel_scales=1.0, sub_size=1
        )

        sersic = am.light_profiles.EllipticalSersic()

        image = sersic.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)

        sersic = am.light_profiles.SphericalSersic()

        image = sersic.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)


class TestExponential:
    def test__constructor_and_units(self):
        exponential = am.light_profiles.EllipticalExponential(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            intensity=1.0,
            effective_radius=0.6,
        )

        assert exponentiam.centre == (1.0, 2.0)
        assert isinstance(exponentiam.centre[0], am.Length)
        assert isinstance(exponentiam.centre[1], am.Length)
        assert exponentiam.centre[0].unit == "arcsec"
        assert exponentiam.centre[1].unit == "arcsec"

        assert exponentiam.axis_ratio == 0.5
        assert isinstance(exponentiam.axis_ratio, float)

        assert exponentiam.phi == 45.0
        assert isinstance(exponentiam.phi, float)

        assert exponentiam.intensity == 1.0
        assert isinstance(exponentiam.intensity, am.Luminosity)
        assert exponentiam.intensity.unit == "eps"

        assert exponentiam.effective_radius == 0.6
        assert isinstance(exponentiam.effective_radius, am.Length)
        assert exponentiam.effective_radius.unit_length == "arcsec"

        assert exponentiam.sersic_index == 1.0
        assert isinstance(exponentiam.sersic_index, float)

        assert exponentiam.sersic_constant == pytest.approx(1.67838, 1e-3)
        assert exponentiam.elliptical_effective_radius == 0.6 / np.sqrt(0.5)

        exponential = am.light_profiles.SphericalExponential(
            centre=(1.0, 2.0), intensity=1.0, effective_radius=0.6
        )

        assert exponentiam.centre == (1.0, 2.0)
        assert isinstance(exponentiam.centre[0], am.Length)
        assert isinstance(exponentiam.centre[1], am.Length)
        assert exponentiam.centre[0].unit == "arcsec"
        assert exponentiam.centre[1].unit == "arcsec"

        assert exponentiam.axis_ratio == 1.0
        assert isinstance(exponentiam.axis_ratio, float)

        assert exponentiam.phi == 0.0
        assert isinstance(exponentiam.phi, float)

        assert exponentiam.intensity == 1.0
        assert isinstance(exponentiam.intensity, am.Luminosity)
        assert exponentiam.intensity.unit == "eps"

        assert exponentiam.effective_radius == 0.6
        assert isinstance(exponentiam.effective_radius, am.Length)
        assert exponentiam.effective_radius.unit_length == "arcsec"

        assert exponentiam.sersic_index == 1.0
        assert isinstance(exponentiam.sersic_index, float)

        assert exponentiam.sersic_constant == pytest.approx(1.67838, 1e-3)
        assert exponentiam.elliptical_effective_radius == 0.6

    def test__intensity_at_radius__correct_value(self):
        exponential = am.light_profiles.EllipticalExponential(
            axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6
        )
        assert exponentiam.profile_image_from_grid_radii(
            grid_radii=1.0
        ) == pytest.approx(0.3266, 1e-3)

        exponential = am.light_profiles.EllipticalExponential(
            axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0
        )
        assert exponentiam.profile_image_from_grid_radii(
            grid_radii=1.5
        ) == pytest.approx(4.5640, 1e-3)

    def test__intensity_from_grid__correct_values(self):
        exponential = am.light_profiles.EllipticalExponential(
            axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0
        )
        assert exponentiam.profile_image_from_grid(
            grid=np.array([[1.0, 0.0]])
        ) == pytest.approx(4.9047, 1e-3)

        exponential = am.light_profiles.EllipticalExponential(
            axis_ratio=0.5, phi=90.0, intensity=2.0, effective_radius=3.0
        )
        assert exponentiam.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(4.8566, 1e-3)

        exponential = am.light_profiles.EllipticalExponential(
            axis_ratio=0.5, phi=90.0, intensity=4.0, effective_radius=3.0
        )
        assert exponentiam.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(2.0 * 4.8566, 1e-3)

    def test__intensity_from_grid__change_geometry(self):
        exponential_0 = am.light_profiles.EllipticalExponential(
            axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0
        )

        exponential_1 = am.light_profiles.EllipticalExponential(
            axis_ratio=0.5, phi=90.0, intensity=3.0, effective_radius=2.0
        )

        assert exponential_0.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == exponential_1.profile_image_from_grid(grid=np.array([[1.0, 0.0]]))

    def test__spherical_and_elliptical_match(self):
        elliptical = am.light_profiles.EllipticalExponential(
            axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0
        )

        spherical = am.light_profiles.SphericalExponential(
            intensity=3.0, effective_radius=2.0
        )

        assert (
            ellipticam.profile_image_from_grid(grid=grid)
            == sphericam.profile_image_from_grid(grid=grid)
        ).all()

    def test__reshape_decorators(self):
        grid = aa.grid.uniform(
            shape_2d=(2, 2), pixel_scales=1.0, sub_size=1
        )

        exponential = am.light_profiles.EllipticalExponential()

        image = exponentiam.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)

        exponential = am.light_profiles.SphericalExponential()

        image = exponentiam.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)


class TestDevVaucouleurs:
    def test__constructor_and_units(self):
        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            intensity=1.0,
            effective_radius=0.6,
        )

        assert dev_vaucouleurs.centre == (1.0, 2.0)
        assert isinstance(dev_vaucouleurs.centre[0], am.Length)
        assert isinstance(dev_vaucouleurs.centre[1], am.Length)
        assert dev_vaucouleurs.centre[0].unit == "arcsec"
        assert dev_vaucouleurs.centre[1].unit == "arcsec"

        assert dev_vaucouleurs.axis_ratio == 0.5
        assert isinstance(dev_vaucouleurs.axis_ratio, float)

        assert dev_vaucouleurs.phi == 45.0
        assert isinstance(dev_vaucouleurs.phi, float)

        assert dev_vaucouleurs.intensity == 1.0
        assert isinstance(dev_vaucouleurs.intensity, am.Luminosity)
        assert dev_vaucouleurs.intensity.unit == "eps"

        assert dev_vaucouleurs.effective_radius == 0.6
        assert isinstance(dev_vaucouleurs.effective_radius, am.Length)
        assert dev_vaucouleurs.effective_radius.unit_length == "arcsec"

        assert dev_vaucouleurs.sersic_index == 4.0
        assert isinstance(dev_vaucouleurs.sersic_index, float)

        assert dev_vaucouleurs.sersic_constant == pytest.approx(7.66924, 1e-3)
        assert dev_vaucouleurs.elliptical_effective_radius == 0.6 / np.sqrt(0.5)

        dev_vaucouleurs = am.light_profiles.SphericalDevVaucouleurs(
            centre=(1.0, 2.0), intensity=1.0, effective_radius=0.6
        )

        assert dev_vaucouleurs.centre == (1.0, 2.0)
        assert isinstance(dev_vaucouleurs.centre[0], am.Length)
        assert isinstance(dev_vaucouleurs.centre[1], am.Length)
        assert dev_vaucouleurs.centre[0].unit == "arcsec"
        assert dev_vaucouleurs.centre[1].unit == "arcsec"

        assert dev_vaucouleurs.axis_ratio == 1.0
        assert isinstance(dev_vaucouleurs.axis_ratio, float)

        assert dev_vaucouleurs.phi == 0.0
        assert isinstance(dev_vaucouleurs.phi, float)

        assert dev_vaucouleurs.intensity == 1.0
        assert isinstance(dev_vaucouleurs.intensity, am.Luminosity)
        assert dev_vaucouleurs.intensity.unit == "eps"

        assert dev_vaucouleurs.effective_radius == 0.6
        assert isinstance(dev_vaucouleurs.effective_radius, am.Length)
        assert dev_vaucouleurs.effective_radius.unit_length == "arcsec"

        assert dev_vaucouleurs.sersic_index == 4.0
        assert isinstance(dev_vaucouleurs.sersic_index, float)

        assert dev_vaucouleurs.sersic_constant == pytest.approx(7.66924, 1e-3)
        assert dev_vaucouleurs.elliptical_effective_radius == 0.6

    def test__intensity_at_radius__correct_value(self):
        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6
        )
        assert dev_vaucouleurs.profile_image_from_grid_radii(
            grid_radii=1.0
        ) == pytest.approx(0.3518, 1e-3)

        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0
        )
        assert dev_vaucouleurs.profile_image_from_grid_radii(
            grid_radii=1.5
        ) == pytest.approx(5.1081, 1e-3)

    def test__intensity_from_grid__correct_values(self):
        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0
        )
        assert dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[1.0, 0.0]])
        ) == pytest.approx(5.6697, 1e-3)

        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=0.5, phi=90.0, intensity=2.0, effective_radius=3.0
        )

        assert dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(7.4455, 1e-3)

        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=0.5, phi=90.0, intensity=4.0, effective_radius=3.0
        )
        assert dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(2.0 * 7.4455, 1e-3)

    def test__intensity_from_grid__change_geometry(self):
        dev_vaucouleurs_0 = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0
        )

        dev_vaucouleurs_1 = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=0.5, phi=90.0, intensity=3.0, effective_radius=2.0
        )

        assert dev_vaucouleurs_0.profile_image_from_grid(
            grid=np.array([[0.0, 1.0]])
        ) == dev_vaucouleurs_1.profile_image_from_grid(grid=np.array([[1.0, 0.0]]))

    def test__spherical_and_elliptical_match(self):
        elliptical = am.light_profiles.EllipticalDevVaucouleurs(
            axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0
        )

        spherical = am.light_profiles.SphericalDevVaucouleurs(
            intensity=3.0, effective_radius=2.0
        )

        assert (
            ellipticam.profile_image_from_grid(grid=grid)
            == sphericam.profile_image_from_grid(grid=grid)
        ).all()

    def test__reshape_decorators(self):
        grid = aa.grid.uniform(
            shape_2d=(2, 2), pixel_scales=1.0, sub_size=1
        )

        dev_vaucouleurs = am.light_profiles.EllipticalDevVaucouleurs()

        image = dev_vaucouleurs.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)

        dev_vaucouleurs = am.light_profiles.SphericalDevVaucouleurs()

        image = dev_vaucouleurs.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)


class TestCoreSersic(object):
    def test__constructor_and_units(self):
        core_sersic = am.light_profiles.EllipticalCoreSersic(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            intensity=1.0,
            effective_radius=0.6,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=2.0,
        )

        assert core_sersic.centre == (1.0, 2.0)
        assert isinstance(core_sersic.centre[0], am.Length)
        assert isinstance(core_sersic.centre[1], am.Length)
        assert core_sersic.centre[0].unit == "arcsec"
        assert core_sersic.centre[1].unit == "arcsec"

        assert core_sersic.axis_ratio == 0.5
        assert isinstance(core_sersic.axis_ratio, float)

        assert core_sersic.phi == 45.0
        assert isinstance(core_sersic.phi, float)

        assert core_sersic.intensity == 1.0
        assert isinstance(core_sersic.intensity, am.Luminosity)
        assert core_sersic.intensity.unit == "eps"

        assert core_sersic.effective_radius == 0.6
        assert isinstance(core_sersic.effective_radius, am.Length)
        assert core_sersic.effective_radius.unit_length == "arcsec"

        assert core_sersic.sersic_index == 4.0
        assert isinstance(core_sersic.sersic_index, float)

        assert core_sersic.radius_break == 0.01
        assert isinstance(core_sersic.radius_break, am.Length)
        assert core_sersic.radius_break.unit_length == "arcsec"

        assert core_sersic.intensity_break == 0.1
        assert isinstance(core_sersic.intensity_break, am.Luminosity)
        assert core_sersic.intensity_break.unit == "eps"

        assert core_sersic.gamma == 1.0
        assert isinstance(core_sersic.gamma, float)

        assert core_sersic.alpha == 2.0
        assert isinstance(core_sersic.alpha, float)

        assert core_sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert core_sersic.elliptical_effective_radius == 0.6 / np.sqrt(0.5)

        core_sersic = am.light_profiles.SphericalCoreSersic(
            centre=(1.0, 2.0),
            intensity=1.0,
            effective_radius=0.6,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=2.0,
        )

        assert core_sersic.centre == (1.0, 2.0)
        assert isinstance(core_sersic.centre[0], am.Length)
        assert isinstance(core_sersic.centre[1], am.Length)
        assert core_sersic.centre[0].unit == "arcsec"
        assert core_sersic.centre[1].unit == "arcsec"

        assert core_sersic.axis_ratio == 1.0
        assert isinstance(core_sersic.axis_ratio, float)

        assert core_sersic.phi == 0.0
        assert isinstance(core_sersic.phi, float)

        assert core_sersic.intensity == 1.0
        assert isinstance(core_sersic.intensity, am.Luminosity)
        assert core_sersic.intensity.unit == "eps"

        assert core_sersic.effective_radius == 0.6
        assert isinstance(core_sersic.effective_radius, am.Length)
        assert core_sersic.effective_radius.unit_length == "arcsec"

        assert core_sersic.sersic_index == 4.0
        assert isinstance(core_sersic.sersic_index, float)

        assert core_sersic.radius_break == 0.01
        assert isinstance(core_sersic.radius_break, am.Length)
        assert core_sersic.radius_break.unit_length == "arcsec"

        assert core_sersic.intensity_break == 0.1
        assert isinstance(core_sersic.intensity_break, am.Luminosity)
        assert core_sersic.intensity_break.unit == "eps"

        assert core_sersic.gamma == 1.0
        assert isinstance(core_sersic.gamma, float)

        assert core_sersic.alpha == 2.0
        assert isinstance(core_sersic.alpha, float)

        assert core_sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert core_sersic.elliptical_effective_radius == 0.6

    def test__intensity_at_radius__correct_value(self):
        core_sersic = am.light_profiles.EllipticalCoreSersic(
            axis_ratio=0.5,
            phi=0.0,
            intensity=1.0,
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
        )
        assert core_sersic.profile_image_from_grid_radii(0.01) == 0.1

    def test__spherical_and_elliptical_match(self):
        elliptical = am.light_profiles.EllipticalCoreSersic(
            axis_ratio=1.0,
            phi=0.0,
            intensity=1.0,
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
        )

        spherical = am.light_profiles.SphericalCoreSersic(
            intensity=1.0,
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
        )

        assert (
            ellipticam.profile_image_from_grid(grid=grid)
            == sphericam.profile_image_from_grid(grid=grid)
        ).all()

    def test__reshape_decorators(self):
        grid = aa.grid.uniform(
            shape_2d=(2, 2), pixel_scales=1.0, sub_size=1
        )

        core_sersic = am.light_profiles.EllipticalCoreSersic()

        image = core_sersic.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)

        core_sersic = am.light_profiles.SphericalCoreSersic()

        image = core_sersic.profile_image_from_grid(grid=grid)

        assert image.in_2d.shape == (2, 2)


def luminosity_from_radius_and_profile(radius, profile):
    x = profile.sersic_constant * (
        (radius / profile.effective_radius) ** (1.0 / profile.sersic_index)
    )

    return (
        profile.intensity
        * profile.effective_radius ** 2
        * 2
        * math.pi
        * profile.sersic_index
        * (
            (math.e ** profile.sersic_constant)
            / (profile.sersic_constant ** (2 * profile.sersic_index))
        )
        * scipy.speciam.gamma(2 * profile.sersic_index)
        * scipy.speciam.gammainc(2 * profile.sersic_index, x)
    )


class TestBlurredProfileImages(object):
    def test__blurred_image_from_grid_and_psf(
        self, sub_grid_7x7, blurring_grid_7x7, psf_3x3, convolver_7x7
    ):

        light_profile = am.light_profiles.EllipticalSersic(intensity=1.0)

        image = light_profile.profile_image_from_grid(grid=sub_grid_7x7)

        blurring_image = light_profile.profile_image_from_grid(grid=blurring_grid_7x7)

        blurred_image = convolver_7x7.convolved_scaled_array_from_image_array_and_blurring_array(
            image_array=image.in_1d_binned, blurring_array=blurring_image.in_1d_binned
        )

        light_profile_blurred_image = light_profile.blurred_profile_image_from_grid_and_psf(
            grid=sub_grid_7x7, blurring_grid=blurring_grid_7x7, psf=psf_3x3
        )

        assert blurred_image.in_1d == pytest.approx(
            light_profile_blurred_image.in_1d, 1.0e-4
        )
        assert blurred_image.in_2d == pytest.approx(
            light_profile_blurred_image.in_2d, 1.0e-4
        )

    def test__blurred_image_from_grid_and_convolver(
        self, sub_grid_7x7, blurring_grid_7x7, convolver_7x7
    ):

        light_profile = am.light_profiles.EllipticalSersic(intensity=1.0)

        image = light_profile.profile_image_from_grid(grid=sub_grid_7x7)

        blurring_image = light_profile.profile_image_from_grid(grid=blurring_grid_7x7)

        blurred_image = convolver_7x7.convolved_image_1d_from_image_array_and_blurring_array(
            image_array=image.in_1d_binned, blurring_array=blurring_image.in_1d_binned
        )

        light_profile_blurred_image = light_profile.blurred_profile_image_from_grid_and_convolver(
            grid=sub_grid_7x7, convolver=convolver_7x7, blurring_grid=blurring_grid_7x7
        )

        assert blurred_image.in_1d == pytest.approx(
            light_profile_blurred_image.in_1d, 1.0e-4
        )
        assert blurred_image.in_2d == pytest.approx(
            light_profile_blurred_image.in_2d, 1.0e-4
        )


class TestVisibilities(object):
    def test__visibilities_from_grid_and_transformer(
        self, grid_7x7, sub_grid_7x7, transformer_7x7_7
    ):
        light_profile = am.light_profiles.EllipticalSersic(intensity=1.0)

        image = light_profile.profile_image_from_grid(grid=grid_7x7)

        visibilities = transformer_7x7_7.visibilities_from_image(
            image=image.in_1d_binned
        )

        light_profile_visibilities = light_profile.profile_visibilities_from_grid_and_transformer(
            grid=grid_7x7, transformer=transformer_7x7_7
        )

        assert visibilities == pytest.approx(light_profile_visibilities, 1.0e-4)


class TestLuminosityWithinCircle(object):
    def test__luminosity_in_eps__spherical_sersic_index_2__compare_to_analytic(self):
        sersic = am.light_profiles.SphericalSersic(
            intensity=3.0, effective_radius=2.0, sersic_index=2.0
        )

        radius = am.Length(0.5, "arcsec")

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic
        )

        luminosity_integral = sersic.luminosity_within_circle_in_units(
            radius=0.5, unit_luminosity="eps"
        )

        assert luminosity_analytic == pytest.approx(luminosity_integral, 1e-3)

    def test__luminosity_in_eps__spherical_sersic_2__compare_to_grid(self):
        sersic = am.light_profiles.SphericalSersic(
            intensity=3.0, effective_radius=2.0, sersic_index=2.0
        )

        radius = am.Length(1.0, "arcsec")

        luminosity_grid = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic
        )

        luminosity_integral = sersic.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity="eps"
        )

        assert luminosity_grid == pytest.approx(luminosity_integral, 0.02)

    def test__luminosity_units_conversions__uses_exposure_time(self):
        sersic_eps = am.light_profiles.SphericalSersic(
            intensity=am.Luminosity(3.0, "eps"), effective_radius=2.0, sersic_index=1.0
        )

        radius = am.Length(0.5, "arcsec")

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic_eps
        )

        luminosity_integral = sersic_eps.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity="eps", exposure_time=3.0
        )

        # eps -> eps

        assert luminosity_analytic == pytest.approx(luminosity_integral, 1e-3)

        # eps -> counts

        luminosity_integral = sersic_eps.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity="counts", exposure_time=3.0
        )

        assert 3.0 * luminosity_analytic == pytest.approx(luminosity_integral, 1e-3)

        sersic_counts = am.light_profiles.SphericalSersic(
            intensity=am.Luminosity(3.0, "counts"),
            effective_radius=2.0,
            sersic_index=1.0,
        )

        radius = am.Length(0.5, "arcsec")

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic_counts
        )
        luminosity_integral = sersic_counts.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity="eps", exposure_time=3.0
        )

        # counts -> eps

        assert luminosity_analytic / 3.0 == pytest.approx(luminosity_integral, 1e-3)

        luminosity_integral = sersic_counts.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity="counts", exposure_time=3.0
        )

        # counts -> counts

        assert luminosity_analytic == pytest.approx(luminosity_integral, 1e-3)

    def test__radius_units_conversions__light_profile_updates_units_and_computes_correct_luminosity(
        self
    ):
        cosmology = mock_cosmology.MockCosmology(arcsec_per_kpc=0.5, kpc_per_arcsec=2.0)

        sersic_arcsec = am.light_profiles.SphericalSersic(
            centre=(am.Length(0.0, "arcsec"), am.Length(0.0, "arcsec")),
            intensity=am.Luminosity(3.0, "eps"),
            effective_radius=am.Length(2.0, "arcsec"),
            sersic_index=1.0,
        )

        sersic_kpc = am.light_profiles.SphericalSersic(
            centre=(am.Length(0.0, "kpc"), am.Length(0.0, "kpc")),
            intensity=am.Luminosity(3.0, "eps"),
            effective_radius=am.Length(4.0, "kpc"),
            sersic_index=1.0,
        )

        radius = am.Length(0.5, "arcsec")

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic_arcsec
        )

        # arcsec -> arcsec

        luminosity = sersic_arcsec.luminosity_within_circle_in_units(radius=radius)

        assert luminosity_analytic == pytest.approx(luminosity, 1e-3)

        # kpc -> arcsec

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=1.0, profile=sersic_kpc
        )

        luminosity = sersic_kpc.luminosity_within_circle_in_units(
            radius=radius, redshift_profile=0.5, cosmology=cosmology
        )

        assert luminosity_analytic == pytest.approx(luminosity, 1e-3)

        radius = am.Length(0.5, "kpc")

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=radius, profile=sersic_kpc
        )

        # kpc -> kpc

        luminosity = sersic_kpc.luminosity_within_circle_in_units(radius=radius)

        assert luminosity_analytic == pytest.approx(luminosity, 1e-3)

        # kpc -> arcsec

        luminosity_analytic = luminosity_from_radius_and_profile(
            radius=0.25, profile=sersic_arcsec
        )

        luminosity = sersic_arcsec.luminosity_within_circle_in_units(
            radius=radius, redshift_profile=0.5, cosmology=cosmology
        )

        assert luminosity_analytic == pytest.approx(luminosity, 1e-3)

        radius = am.Length(2.0, "arcsec")
        luminosity_arcsec = sersic_arcsec.luminosity_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            unit_mass="angular",
            cosmology=cosmology,
        )
        radius = am.Length(4.0, "kpc")
        luminosity_kpc = sersic_arcsec.luminosity_within_circle_in_units(
            radius=radius,
            redshift_profile=0.5,
            unit_mass="angular",
            cosmology=cosmology,
        )
        assert luminosity_arcsec == luminosity_kpc


class TestLuminosityWithinEllipse(object):
    def test__within_ellipse_in_counts__check_multiplies_by_exposure_time(self):

        sersic = am.light_profiles.EllipticalSersic(
            axis_ratio=0.5,
            phi=90.0,
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
        )

        radius = am.Length(0.5, "arcsec")
        luminosity_grid = 0.0

        xs = np.linspace(-1.8, 1.8, 80)
        ys = np.linspace(-1.8, 1.8, 80)

        edge = xs[1] - xs[0]
        area = edge ** 2

        for x in xs:
            for y in ys:

                eta = sersic.grid_to_elliptical_radii(np.array([[x, y]]))

                if eta < radius:
                    luminosity_grid += sersic.profile_image_from_grid_radii(eta) * area

        luminosity_integral = sersic.luminosity_within_ellipse_in_units(
            major_axis=radius, unit_luminosity="counts", exposure_time=3.0
        )

        assert 3.0 * luminosity_grid[0] == pytest.approx(luminosity_integral, 0.02)


class TestGrids(object):
    def test__grid_to_eccentric_radius(self):
        elliptical = am.light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0)

        assert ellipticam.grid_to_eccentric_radii(np.array([[1, 1]])) == pytest.approx(
            ellipticam.grid_to_eccentric_radii(np.array([[-1, -1]])), 1e-10
        )

    def test__intensity_from_grid(self):
        elliptical = am.light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0)

        assert ellipticam.profile_image_from_grid(np.array([[1, 1]])) == pytest.approx(
            ellipticam.profile_image_from_grid(np.array([[-1, -1]])), 1e-4
        )
