import docker
import threading
import sys
import time
from skopt import gp_minimize
from skopt.plots import plot_convergence
import matplotlib.pyplot as plt
import plot_generator
import joint_plot_generator
import resolution_comparison
import utilities
import QSV_H264
import QSV_VP9
import H264
import X264
import VP9
import FFE

width = '640'
height = '480'

N_CALLS = 100

config = 0

INITIAL_WIDTH = '2048'
INITIAL_HEIGHT = '1536'


def build():
    def build_ffe():
        try:
            docker_client.images.get(FFE.TAG)
            print('Found ' + FFE.TAG + ' image locally')
        except docker.errors.ImageNotFound:
            print(
                'Building ' + FFE.TAG + ' from ' + FFE.REPO + '#' + FFE.VERSION + '. It may take some time...')
            image = docker_client.images.build(path=FFE.REPO + '#' + FFE.VERSION,
                                               dockerfile='Dockerfile.amd64',
                                               tag=FFE.TAG,
                                               rm=True,
                                               forcerm=True
                                               )
            for x in image[1]:
                print(x)
        except Exception as e:
            sys.exit(e)  # Exits script in case of failure to retrieve image

    def build_encoder():
        try:
            docker_client.images.get(encoder.TAG)
            print('Found ' + encoder.TAG + ' image locally')
        except docker.errors.ImageNotFound:
            print(
                'Building ' + encoder.TAG + ' from ' + encoder.REPO + '#' + encoder.VERSION +
                '. It may take some time...')
            image = docker_client.images.build(path=encoder.REPO + '#' + encoder.VERSION,
                                               dockerfile='Dockerfile.amd64',
                                               tag=encoder.TAG,
                                               rm=True,
                                               forcerm=True
                                               )
            for x in image[1]:
                print(x)
        except Exception as e:
            sys.exit(e)

    thread_build_ffe = threading.Thread(target=build_ffe)
    thread_build_encoder = threading.Thread(target=build_encoder)

    thread_build_ffe.start()
    thread_build_encoder.start()

    thread_build_ffe.join()  # Blocks execution until both threads has terminated
    thread_build_encoder.join()


def update_report_name_callback(_):
    global config
    if config < N_CALLS:
        config += 1
    else:
        config = 0

    report_name = utilities.generate_report_name(tag=encoder.TAG, resolution_name=resolution_name,
                                                 config=config)
    FFE.set_report_name(report_name)
    encoder.set_report_name(report_name)


if __name__ == '__main__':
    docker_client = docker.from_env()

    encoders = [VP9, H264, QSV_H264, QSV_VP9] # QSV_VP9 not avail on Brick, FFE fails on encode on X264

    datasets = utilities.get_datasets()
    if not datasets:
        print("No folders found in " + utilities.DATASETS_PATH)
        sys.exit("Exiting..")
    else:
        print("Following datasets are to be evaluated: " + str(datasets))

    utilities.set_run_name()

    for dataset in datasets:
        utilities.set_system_timeout(dataset)
        utilities.set_dataset(dataset)
        utilities.update_run_paths()

        joint_plot_encoders = []

        for encoder in encoders:
            build()  # build FFE and encoder in case they cannot be found locally

            best_configs = []

            for (_, res) in enumerate(utilities.RESOLUTIONS):
                plt.close('all')  # Cleans pyplot's memory before each iteration

                resolution_name = res[0]
                width = res[1]
                height = res[2]
                utilities.set_max_ssim(0)  # reset max_ssim and best_config_name for each resolution
                utilities.set_best_config_name('not_set')

                encoder.initialize(init_width=INITIAL_WIDTH, init_height=INITIAL_HEIGHT, resolution=res,
                                   docker_client=docker_client)
                FFE.initialize(init_width=INITIAL_WIDTH, init_height=INITIAL_HEIGHT, width=width, height=height)

                update_report_name_callback(_)

                start = time.time()

                minimize_result = gp_minimize(func=encoder.objective,
                                              dimensions=encoder.SPACE,
                                              base_estimator=None,
                                              n_calls=N_CALLS,
                                              n_random_starts=10,
                                              acq_func="gp_hedge",
                                              acq_optimizer="auto",
                                              x0=encoder.get_default_encoder_config(resolution_name),
                                              y0=None,
                                              random_state=None,
                                              verbose=True,
                                              callback=update_report_name_callback,
                                              n_points=10000,
                                              n_restarts_optimizer=5,
                                              xi=0.01,
                                              kappa=1.96,
                                              noise="gaussian",
                                              n_jobs=1,
                                              )

                now = time.time()

                print("Best score=%.4f" % minimize_result.fun)
                print("Best parameters:")

                best_parameters = []
                i = 0
                for value in minimize_result.x:
                    best_parameters.append(encoder.PARAMETERS[i] + ': ' + str(value) + '\n')
                    print(encoder.PARAMETERS[i] + ': ' + str(value))  # prints parameters that obtained the highest SSIM
                    i += 1
                print("Best config: " + utilities.get_best_config_name())
                print("It took: ", str((now - start) / 60), " minutes")

                ax = plot_convergence(minimize_result)
                utilities.save_convergence(axes=ax, encoder=encoder, resolution_name=resolution_name)

                utilities.save_list(best_parameters, utilities.get_best_config_name())

                best_config_report_path = utilities.get_output_report_path() + '/' + utilities.get_best_config_name()
                best_config_name = utilities.get_best_config_name()

                # Only append list with configs to be plotted if they are valid
                if utilities.check_config_and_path(best_config_report_path, best_config_name, encoder.TAG,
                                                   resolution_name):
                    best_configs.append(utilities.BestConfig(
                        best_config_report_path=best_config_report_path,
                        best_config_name=best_config_name,
                        resolution_name=resolution_name))

            # Runs the plot_generator script to generate a performance graph of the current encoder and all resolutions
            plot_generator.run(best_configs=best_configs, dataset=utilities.get_dataset_name(), codec=encoder.TAG)

            # Add an Encoder object after each encoders' full execution on a dataset
            joint_plot_encoders.append(utilities.Encoder(
                best_configs=best_configs,
                encoder=encoder.TAG,
                dataset_name=utilities.get_dataset_name()))

        # Runs the joint_plot_generator script to generate a comparision graph of respective encoder's SSIM per res
        joint_plot_generator.run(joint_plot_encoders)
        resolution_comparison.run(joint_plot_encoders)

