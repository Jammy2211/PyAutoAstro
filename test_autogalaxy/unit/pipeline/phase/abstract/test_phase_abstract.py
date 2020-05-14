import autofit as af
import autogalaxy as ag
import pytest
from test_autolens.mock import mock_pipeline

pytestmark = pytest.mark.filterwarnings(
    "ignore:Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of "
    "`arr[seq]`. In the future this will be interpreted as an arrays index, `arr[np.arrays(seq)]`, which will result "
    "either in an error or a different result."
)


class TestModel:
    def test__set_instances(self, phase_dataset_7x7):
        phase_dataset_7x7.galaxies = [ag.Galaxy(redshift=0.5)]
        assert phase_dataset_7x7.model.galaxies == [ag.Galaxy(redshift=0.5)]

    def test__set_models(self, phase_dataset_7x7):
        phase_dataset_7x7.galaxies = [ag.GalaxyModel(redshift=0.5)]
        assert phase_dataset_7x7.model.galaxies == [ag.GalaxyModel(redshift=0.5)]

    def test__promise_attrbutes(self):
        phase = ag.PhaseDataset(
            galaxies=dict(
                lens=ag.GalaxyModel(
                    redshift=0.5,
                    mass=ag.mp.EllipticalIsothermal,
                    shear=ag.mp.ExternalShear,
                ),
                source=ag.GalaxyModel(redshift=1.0, light=ag.lp.EllipticalSersic),
            ),
            non_linear_class=mock_pipeline.MockNLO,
            phase_tag="",
            phase_name="test_phase",
        )

        print(hasattr(af.last.result.instance.galaxies.lens, "mas2s"))

    def test__customize(self, imaging_7x7, mask_7x7):
        class MyPlanePhaseAnd(ag.PhaseImaging):
            def customize_priors(self, results):
                self.galaxies = results.last.instance.galaxies

        results = mock_pipeline.MockResults()

        galaxy = ag.Galaxy(redshift=0.5)
        galaxy_model = ag.GalaxyModel(redshift=0.5)

        setattr(results[0].instance, "galaxies", [galaxy])
        setattr(results[0].model, "galaxies", [galaxy_model])

        phase_dataset_7x7 = MyPlanePhaseAnd(
            phase_name="test_phase", non_linear_class=mock_pipeline.MockNLO
        )

        phase_dataset_7x7.make_analysis(
            dataset=imaging_7x7, mask=mask_7x7, results=results
        )
        phase_dataset_7x7.customize_priors(results=results)

        assert phase_dataset_7x7.galaxies == [galaxy]

        class MyPlanePhaseAnd(ag.PhaseImaging):
            def customize_priors(self, results):
                self.galaxies = results.last.model.galaxies

        results = mock_pipeline.MockResults()

        galaxy = ag.Galaxy(redshift=0.5)
        galaxy_model = ag.GalaxyModel(redshift=0.5)

        setattr(results[0].instance, "galaxies", [galaxy])
        setattr(results[0].model, "galaxies", [galaxy_model])

        phase_dataset_7x7 = MyPlanePhaseAnd(
            phase_name="test_phase", non_linear_class=mock_pipeline.MockNLO
        )

        phase_dataset_7x7.make_analysis(
            dataset=imaging_7x7, mask=mask_7x7, results=results
        )
        phase_dataset_7x7.customize_priors(results)

        assert phase_dataset_7x7.galaxies == [galaxy_model]

    def test__duplication(self):
        phase_dataset_7x7 = ag.PhaseImaging(
            phase_name="test_phase",
            galaxies=dict(
                lens=ag.GalaxyModel(redshift=0.5), source=ag.GalaxyModel(redshift=1.0)
            ),
        )

        ag.PhaseImaging(phase_name="test_phase")

        assert phase_dataset_7x7.galaxies is not None

    def test__phase_can_receive_list_of_galaxy_models(self):
        phase_dataset_7x7 = ag.PhaseImaging(
            galaxies=dict(
                lens=ag.GalaxyModel(
                    sersic=ag.lp.EllipticalSersic,
                    sis=ag.mp.SphericalIsothermal,
                    redshift=ag.Redshift,
                ),
                lens1=ag.GalaxyModel(
                    sis=ag.mp.SphericalIsothermal, redshift=ag.Redshift
                ),
            ),
            non_linear_class=af.MultiNest,
            phase_name="test_phase",
        )

        for item in phase_dataset_7x7.model.path_priors_tuples:
            print(item)

        sersic = phase_dataset_7x7.model.galaxies[0].sersic
        sis = phase_dataset_7x7.model.galaxies[0].sis
        lens_1_sis = phase_dataset_7x7.model.galaxies[1].sis

        arguments = {
            sersic.centre[0]: 0.2,
            sersic.centre[1]: 0.2,
            sersic.axis_ratio: 0.0,
            sersic.phi: 0.1,
            sersic.effective_radius.priors[0]: 0.2,
            sersic.sersic_index: 0.6,
            sersic.intensity.priors[0]: 0.6,
            sis.centre[0]: 0.1,
            sis.centre[1]: 0.2,
            sis.einstein_radius.priors[0]: 0.3,
            phase_dataset_7x7.model.galaxies[0].redshift.priors[0]: 0.4,
            lens_1_sis.centre[0]: 0.6,
            lens_1_sis.centre[1]: 0.5,
            lens_1_sis.einstein_radius.priors[0]: 0.7,
            phase_dataset_7x7.model.galaxies[1].redshift.priors[0]: 0.8,
        }

        instance = phase_dataset_7x7.model.instance_for_arguments(arguments=arguments)

        assert instance.galaxies[0].sersic.centre[0] == 0.2
        assert instance.galaxies[0].sis.centre[0] == 0.1
        assert instance.galaxies[0].sis.centre[1] == 0.2
        assert instance.galaxies[0].sis.einstein_radius == 0.3
        assert instance.galaxies[0].redshift == 0.4
        assert instance.galaxies[1].sis.centre[0] == 0.6
        assert instance.galaxies[1].sis.centre[1] == 0.5
        assert instance.galaxies[1].sis.einstein_radius == 0.7
        assert instance.galaxies[1].redshift == 0.8

        class LensPlanePhase2(ag.PhaseImaging):
            # noinspection PyUnusedLocal
            def pass_models(self, results):
                self.galaxies[0].sis.einstein_radius = 10.0

        phase_dataset_7x7 = LensPlanePhase2(
            galaxies=dict(
                lens=ag.GalaxyModel(
                    sersic=ag.lp.EllipticalSersic,
                    sis=ag.mp.SphericalIsothermal,
                    redshift=ag.Redshift,
                ),
                lens1=ag.GalaxyModel(
                    sis=ag.mp.SphericalIsothermal, redshift=ag.Redshift
                ),
            ),
            non_linear_class=af.MultiNest,
            phase_name="test_phase",
        )

        # noinspection PyTypeChecker
        phase_dataset_7x7.pass_models(None)

        sersic = phase_dataset_7x7.model.galaxies[0].sersic
        sis = phase_dataset_7x7.model.galaxies[0].sis
        lens_1_sis = phase_dataset_7x7.model.galaxies[1].sis

        arguments = {
            sersic.centre[0]: 0.01,
            sersic.centre[1]: 0.2,
            sersic.axis_ratio: 0.0,
            sersic.phi: 0.1,
            sersic.effective_radius.priors[0]: 0.2,
            sersic.sersic_index: 0.6,
            sersic.intensity.priors[0]: 0.6,
            sis.centre[0]: 0.1,
            sis.centre[1]: 0.2,
            phase_dataset_7x7.model.galaxies[0].redshift.priors[0]: 0.4,
            lens_1_sis.centre[0]: 0.6,
            lens_1_sis.centre[1]: 0.5,
            lens_1_sis.einstein_radius.priors[0]: 0.7,
            phase_dataset_7x7.model.galaxies[1].redshift.priors[0]: 0.8,
        }

        instance = phase_dataset_7x7.model.instance_for_arguments(arguments)

        assert instance.galaxies[0].sersic.centre[0] == 0.01
        assert instance.galaxies[0].sis.centre[0] == 0.1
        assert instance.galaxies[0].sis.centre[1] == 0.2
        assert instance.galaxies[0].sis.einstein_radius == 10.0
        assert instance.galaxies[0].redshift == 0.4
        assert instance.galaxies[1].sis.centre[0] == 0.6
        assert instance.galaxies[1].sis.centre[1] == 0.5
        assert instance.galaxies[1].sis.einstein_radius == 0.7
        assert instance.galaxies[1].redshift == 0.8


class TestSetup:

    # noinspection PyTypeChecker
    def test_assertion_failure(self, imaging_7x7, mask_7x7):
        def make_analysis(*args, **kwargs):
            return mock_pipeline.GalaxiesMockAnalysis(1, 1)

        phase_dataset_7x7 = ag.PhaseImaging(
            phase_name="phase_name",
            non_linear_class=mock_pipeline.MockNLO,
            galaxies=dict(
                lens=ag.Galaxy(light=ag.lp.EllipticalLightProfile, redshift=1)
            ),
        )

        phase_dataset_7x7.make_analysis = make_analysis
        result = phase_dataset_7x7.run(dataset=imaging_7x7, results=None, mask=None)
        assert result is not None

        phase_dataset_7x7 = ag.PhaseImaging(
            phase_name="phase_name",
            non_linear_class=mock_pipeline.MockNLO,
            galaxies=dict(
                lens=ag.Galaxy(light=ag.lp.EllipticalLightProfile, redshift=1)
            ),
        )

        phase_dataset_7x7.make_analysis = make_analysis
        result = phase_dataset_7x7.run(dataset=imaging_7x7, results=None, mask=None)
        assert result is not None

        class CustomPhase(ag.PhaseImaging):
            def customize_priors(self, results):
                self.galaxies.lens.light = ag.lp.EllipticalLightProfile()

        phase_dataset_7x7 = CustomPhase(
            phase_name="phase_name",
            non_linear_class=mock_pipeline.MockNLO,
            galaxies=dict(
                lens=ag.Galaxy(light=ag.lp.EllipticalLightProfile, redshift=1)
            ),
        )
        phase_dataset_7x7.make_analysis = make_analysis

        # with pytest.raises(af.exc.PipelineException):
        #     phase_dataset_7x7.run(data=imaging_7x7, results=None, mask=None)
