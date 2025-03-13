import numpy
import XCoreModeling
import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.analysis as analysis
import s4l_v1.materials.database as database
import s4l_v1.simulation.neuron as neuron
import s4l_v1.units as units
from s4l_v1 import ReleaseVersion
from s4l_v1 import Unit
import time

def map_components_and_entities():
    return true

def add_axon_setting(simulation):
    return true

def add_points_sensor_settings(simulation):
    return true
    

def add_source_setting(simulation, source, FrequencySine=24000, AmplitudeSine=20.0, NumberOfHalfPeriodsSine=12000):
    source_settings = simulation.AddGenericSource([source])
    source_settings.PulseType = source_settings.PulseType.enum.Sinusoidal
    source_settings.FrequencySine = FrequencySine, units.Hz
    source_settings.AmplitudeSine = AmplitudeSine
    source_settings.NumberOfHalfPeriodsSine = NumberOfHalfPeriodsSine

def add_solver_setting(simulation):
    solver_settings = simulation.SolverSettings
    solver_settings.NumberOfThreads = 8
    solver_settings.Duration = 0.003, units.Seconds

def titration_extractor(simulation):
    simulation_extractor_2 = simulation.Results()
    # Adding a new SensorExtractor
    sensor_extractor = simulation_extractor_2["Titration Sensor"]
    document.AllAlgorithms.Add(sensor_extractor)
    
    # Adding a new TitrationEvaluator
    inputs = [sensor_extractor.Outputs["Titration"]]
    titration_evaluator = analysis.neuron_evaluators.TitrationEvaluator(inputs=inputs)
    titration_evaluator.UpdateAttributes()
    document.AllAlgorithms.Add(titration_evaluator)

    # Get update titration result
    import time
    while not titration_evaluator.Outputs["Titration"].Update():
        time.sleep(4)

    results = titration_evaluator.TitrationData()
    for result in results:
        print(result.TitrationFactor)

def run_simulation_with_settings(FrequencySine=24000, AmplitudeSine=20.0, NumberOfHalfPeriodsSine=12000):
    import s4l_v1.model as model
    
    # Create the simulation
    simulation = neuron.Simulation()

    # Mapping the components and entities
    entity__nerve_dorsal_root_spinal_c5__brachial_plexus_radial_right_6_sweeney_neuron2000um = model.AllEntities()["Nerve_dorsal_root_spinal_C5_Brachial_plexus_radial_right_ 6 [Sweeney Neuron 20.00um]"]
    entity__nerve_ventral_root_spinal_t1__brachial_plexus_ulnar_right_6_sweeney_neuron2000um = model.AllEntities()["Nerve_ventral_root_spinal_T1_Brachial_plexus_ulnar_right_ 6 [Sweeney Neuron 20.00um]"]
    entity__nerve_ventral_root_spinal_c8__brachial_plexus_median_right_3_sweeney_neuron2000um = model.AllEntities()["Nerve_ventral_root_spinal_C8_Brachial_plexus_median_right_ 3 [Sweeney Neuron 20.00um]"]
    
    # Link source
    link_0_overall_field = document.AllSimulations["EM Simulations"].AllComponents["Overall Field"]

    # Add Axon settings (automatic)
    automatic_axon_neuron_settings = neuron.AutomaticAxonNeuronSettings()
    components = [entity__nerve_dorsal_root_spinal_c5__brachial_plexus_radial_right_6_sweeney_neuron2000um, entity__nerve_ventral_root_spinal_c8__brachial_plexus_median_right_3_sweeney_neuron2000um, entity__nerve_ventral_root_spinal_t1__brachial_plexus_ulnar_right_6_sweeney_neuron2000um]
    simulation.Add(automatic_axon_neuron_settings, components)

    # Add points sensor settings
    # Add points sensor
    # Ventral Spinal T1 Brachial Plexus Ulnar right
    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_t1__brachial_plexus_ulnar_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[114]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_t1__brachial_plexus_ulnar_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[150]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_t1__brachial_plexus_ulnar_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[60]"

    # Ventral Spinal C8 Brachial Plexus Median Right
    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_c8__brachial_plexus_median_right_3_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[114]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_c8__brachial_plexus_median_right_3_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[60]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_ventral_root_spinal_c8__brachial_plexus_median_right_3_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[152]"

    # Dorsal Spinal C5 Brachial Plexus Radial Right
    point_sensor_settings = simulation.AddPointSensor([entity__nerve_dorsal_root_spinal_c5__brachial_plexus_radial_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[112]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_dorsal_root_spinal_c5__brachial_plexus_radial_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[55]"

    point_sensor_settings = simulation.AddPointSensor([entity__nerve_dorsal_root_spinal_c5__brachial_plexus_radial_right_6_sweeney_neuron2000um])
    point_sensor_settings.SectionName = u"node[140]"

    # Source settings
    add_source_setting(simulation, source=link_0_overall_field, FrequencySine=FrequencySine, AmplitudeSine=AmplitudeSine, NumberOfHalfPeriodsSine=NumberOfHalfPeriodsSine)

    # Solver settings
    add_solver_setting(simulation)

    document.AllSimulations.Add( simulation )

    # Run the simulation
    simulation.RunSimulation()

    # Sleep to allow for execution to finish
    time.sleep(10)
    
    # Extract the values
    titration_extractor(simulation)
    
def main():
    frequenciesList = [10000, 15000, 20000]
    halfPeriodsList = frequenciesList
    amplitudesList = [20, 20, 20]

    for frequency, period, amplitude in zip(frequenciesList, halfPeriodsList, amplitudesList):
        run_simulation_with_settings(FrequencySine=frequency, NumberOfHalfPeriodsSine=period, AmplitudeSine = amplitude)

if __name__ == "__main__":
    # Define the version to use for default values
    ReleaseVersion.set_active(ReleaseVersion.version8_2)
    # Set active model
    main()
    

