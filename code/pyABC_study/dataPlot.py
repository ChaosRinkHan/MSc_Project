import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyabc

from pyABC_study.ODE import ODESolver, exp_data_s, exp_data_SEM


# rawData_path = os.path.abspath(os.curdir) + "/data/rawData.csv"
# rawData = pd.read_csv(rawData_path).astype("float32")


def quantile_calculate(all_data, length, q=0.5):
    """
Calculate quantiles
    :param all_data: all data
    :param length: time length
    :param q: quantile
    :return: data frame of the quantile
    """
    df_quantile = pd.DataFrame(columns=['N', 'M', 'B', 'A'])
    for jj in range(length):
        # print(df_all_sim_data.loc[jj].mean())
        df_quantile = df_quantile.append(all_data.loc[jj].quantile(q), ignore_index=True)
    # print(df_quantile)
    return df_quantile


def obs_data_plot(time_points: np.array, obs_data_raw):
    """
    Plot the data of dict type
    :param time_points: time points to plot
    :param obs_data_noisy: data in duct type
    :return:
    """
    plt.plot(time_points, obs_data_raw['B'], alpha=0.5, label='Raw beta')
    plt.plot(time_points, obs_data_raw['A'], alpha=0.5, label='Raw alpha')
    plt.legend()
    plt.show()


def result_plot(history, true_parameter: dict, limits: pyabc.Distribution, nr_population=1, savefig=False):
    """
Plot the population distribution, eps values and acceptance rate
    :param limits: Limits of the plot
    :param true_parameter: true parameter
    :param history: pyABC history object
    :param nr_population: the population to be plotted
    :return:
    """

    # pyabc.visualization.plot_acceptance_rates_trajectory(history)
    # if savefig:
    #     plt.savefig("acceptanceRates.png", dpi=200)
    # plt.show()
    #
    # pyabc.visualization.plot_epsilons(history)
    # if savefig:
    #     plt.savefig("eps.png", dpi=200)
    # plt.show()

    df, w = history.get_distribution(t=nr_population)

    for key in df.keys():
        print(key + ", Inter-quartile [%.3f, %.3f], Mean %.3f" % (
            df[key].quantile(0.25), df[key].quantile(0.75), df[key].mean()))

    # Parameters in the first equation

    fig, ax = plt.subplots(1, 5, figsize=(20, 4))
    idx = 0
    for keys in ['lambda_n', 'a', 'k_n_beta', 'mu_n', 'v_n_phi']:
        # print(keys+": %.2f" % true_parameter[keys])
        pyabc.visualization.plot_kde_1d(df, w, x=keys, ax=ax[idx], size=(20, 4))  # xmin=limits[keys].args[0],
        # xmax=limits[keys].args[0] + limits[keys].args[1])
        if true_parameter is not None:
            ax[idx].axvline(true_parameter[keys], color='r', linestyle='dashed',
                            label="True value\n%.3f" % true_parameter[keys])
        ax[idx].axvspan(df[keys].quantile(0.25), df[keys].quantile(0.75), color="b", alpha=0.5,
                        label="Inter-quartile: [%.3f, %.3f]" % (
                            df[keys].quantile(0.25), df[keys].quantile(0.75)))
        ax[idx].legend(loc=8, bbox_to_anchor=(0.5, 1), frameon=False)
        idx += 1
    # fig.suptitle
    plt.subplots_adjust(wspace=1)
    if savefig:
        plt.savefig("para1.png", dpi=200)
    plt.show()

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    idx = 0
    for keys in ['k_phi_beta', 'mu_phi']:
        pyabc.visualization.plot_kde_1d(df, w, x=keys, ax=ax[idx], size=(8, 4))#, xmin=limits[keys].args[0],
                                        # xmax=limits[keys].args[0] + limits[keys].args[1])
        if true_parameter is not None:
            ax[idx].axvline(true_parameter[keys], color='r', linestyle='dashed',
                            label="True value\n%.3f" % true_parameter[keys])
        ax[idx].axvspan(df[keys].quantile(0.25), df[keys].quantile(0.75), color="b", alpha=0.5,
                        label="Inter-quartile: [%.3f, %.3f]" % (
                            df[keys].quantile(0.25), df[keys].quantile(0.75)))
        ax[idx].legend(loc=8, bbox_to_anchor=(0.5, 1), frameon=False)
        idx += 1
    # fig.suptitle('ODE 2: d(Phi)/dt')
    if savefig:
        plt.savefig("para2.png", dpi=200)
    plt.subplots_adjust(wspace=1)
    plt.show()

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    idx = 0
    for keys in ['s_beta_n', 'mu_beta']:
        pyabc.visualization.plot_kde_1d(df, w, x=keys, ax=ax[idx], size=(8, 4)) #,xmin=limits[keys].args[0],
                                        # xmax=limits[keys].args[0] + limits[keys].args[1])
        if true_parameter is not None:
            ax[idx].axvline(true_parameter[keys], color='r', linestyle='dashed',
                            label="True value\n%.3f" % true_parameter[keys])
        ax[idx].axvspan(df[keys].quantile(0.25), df[keys].quantile(0.75), color="b", alpha=0.5,
                        label="Inter-quartile: [%.3f, %.3f]" % (
                            df[keys].quantile(0.25), df[keys].quantile(0.75)))
        ax[idx].legend(loc=8, bbox_to_anchor=(0.5, 1), frameon=False)
        idx += 1
    # fig.suptitle('ODE 3: d(beta)/dt')
    plt.subplots_adjust(wspace=1)
    if savefig:
        plt.savefig("para3.png", dpi=200)
    plt.show()

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    idx = 0
    for keys in ['s_alpha_phi', 'mu_alpha']:
        pyabc.visualization.plot_kde_1d(df, w, x=keys, ax=ax[idx], size=(8, 4)),# xmin=limits[keys].args[0],
                                        # xmax=limits[keys].args[0] + limits[keys].args[1])
        if true_parameter is not None:
            ax[idx].axvline(true_parameter[keys], color='r', linestyle='dashed',
                            label="True value\n%.3f" % true_parameter[keys])
        ax[idx].axvspan(df[keys].quantile(0.25), df[keys].quantile(0.75), color="b", alpha=0.5,
                        label="Inter-quartile: [%.3f, %.3f]" % (
                            df[keys].quantile(0.25), df[keys].quantile(0.75)))
        ax[idx].legend(loc=8, bbox_to_anchor=(0.5, 1), frameon=False)
        idx += 1
    # fig.suptitle('ODE 4: d(alpha)/dt')
    plt.subplots_adjust(wspace=1)
    if savefig:
        plt.savefig("para4.png", dpi=200)
    plt.show()

    # pyabc.visualization.plot_credible_intervals(history, size=(8, 24))
    # if savefig:
    #     plt.savefig("credibleIntervals.png", dpi=200)
    # plt.show()
    #
    # pyabc.visualization.plot_sample_numbers(history)
    # if savefig:
    #     plt.savefig("nr_samples.png", dpi=200)
    # plt.show()
    #
    # pyabc.visualization.plot_effective_sample_sizes(history)
    # if savefig:
    #     plt.savefig("ESS.png", dpi=200)
    # plt.show()

    # pyabc.visualization.plot_kde_matrix(df, w)
    # if savefig:
    #     plt.savefig("joint.png", dpi=200)
    # plt.show()


def result_data(history, solver: ODESolver, compare_data=exp_data_s, nr_population=1, sample_size=500, savefig=False):
    """
Visualise SMC population and compare it with target data
    :param history: abc.history object
    :param compare_data: target data
    :param nr_population: the id of population to be visualised
    :param sample_size: sampling size of the selected population
    """
    df, w = history.get_distribution(t=nr_population)
    # if is_old:
    #     df.columns = ['i_beta_phi', 'k_phi_beta', 'k_n_beta', 'lambda_phi', 'lambda_n', 'mu_alpha', 'mu_beta', 'mu_phi',
    #                   'mu_n', 's_alpha_phi', 's_beta_n', 'v_n_phi']
    df_sample = df.sample(sample_size, replace=False)
    df_all_sim_data = pd.DataFrame(columns=['N', 'M', 'B', 'A'])

    solver.time_point = solver.time_point_default
    for ii in range(sample_size):
        temp_dict = df_sample.iloc[ii].to_dict()
        sim_data = solver.ode_model(temp_dict, flatten=False)
        # print(sim_data)
        sim_data = pd.DataFrame.from_dict(sim_data)
        df_all_sim_data = pd.concat([df_all_sim_data, sim_data])

    # plt.ylim(0, 2) # TODO make lim a function parameter
    # plt.show()

    df_mean = pd.DataFrame(columns=['N', 'M', 'B', 'A'])
    for jj in range(solver.time_point.__len__()):
        # print(df_all_sim_data.loc[jj].mean())
        df_mean = df_mean.append(df_all_sim_data.loc[jj].mean(), ignore_index=True)

    df_median = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.5)
    df_75 = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.75)
    df_25 = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.25)

    fig, axs = plt.subplots(4, 1, figsize=(6, 12))
    plt.subplots_adjust(hspace=0.5)
    index_cov = ['N', 'M', 'B', 'A']
    titles = ["N", "Φ", "β", "α"]
    for kk in range(4):
        seq_mask = np.isfinite(compare_data[index_cov[kk]])
        # axs[kk].plot(solver.timePoint, df_25.iloc[:, kk], 'b--')
        # axs[kk].plot(solver.timePoint, df_75.iloc[:, kk], 'b--')
        axs[kk].fill_between(solver.time_point, df_25.iloc[:, kk], df_75.iloc[:, kk], alpha=0.9, color='lightgrey',
                             label='25% – 75% quantile range')
        axs[kk].plot(solver.time_point, df_mean.iloc[:, kk], 'b', label="Mean", alpha=0.6)
        axs[kk].scatter(solver.time_point_exp[seq_mask], compare_data[index_cov[kk]][seq_mask], alpha=0.7, marker='^',
                        color='black', label='Observed')
        axs[kk].errorbar(solver.time_point_exp, compare_data[index_cov[kk]],
                         yerr=[[0.5 * x for x in exp_data_SEM[index_cov[kk]]],
                               [0.5 * x for x in exp_data_SEM[index_cov[kk]]]], fmt='none',
                         ecolor='grey', elinewidth=2, alpha=0.6)
        # axs[kk].legend(['Mean', '25% – 75% quantile range', 'Observed'])
        axs[kk].set_title(titles[kk])
    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center')
    # fig.tight_layout(pad=5.0)
    if savefig:
        plt.savefig("resultCurve.png", dpi=200)
    # plt.subplots_adjust(hspace=5.5)
    plt.show()


def result_data_old(history, solver: ODESolver, compare_data=exp_data_s, nr_population=1, sample_size=500, savefig=False,
                    is_old=False):
    """
Visualise SMC population and compare it with target data
    :param history: abc.history object
    :param compare_data: target data
    :param nr_population: the id of population to be visualised
    :param sample_size: sampling size of the selected population
    """
    df, w = history.get_distribution(t=nr_population)
    # df.columns = ['i_beta_phi', 'k_phi_beta', 'k_n_beta', 'lambda_phi', 'lambda_n', 'mu_alpha', 'mu_beta', 'mu_phi',
    #               'mu_n', 's_alpha_phi', 's_beta_n', 'v_n_phi']

    df_sample = df.sample(sample_size, replace=False)
    df_all_sim_data = pd.DataFrame(columns=['N', 'M', 'B', 'A'])

    solver.time_point = solver.time_point_default
    for ii in range(sample_size):
        temp_dict = df_sample.iloc[ii].to_dict()
        sim_data = solver.ode_model(temp_dict, flatten=False)
        # print(sim_data)
        sim_data = pd.DataFrame.from_dict(sim_data)
        df_all_sim_data = pd.concat([df_all_sim_data, sim_data])

    # plt.ylim(0, 2) # TODO make lim a function parameter
    # plt.show()

    df_mean = pd.DataFrame(columns=['N', 'M', 'B', 'A'])
    for jj in range(solver.time_point.__len__()):
        # print(df_all_sim_data.loc[jj].mean())
        df_mean = df_mean.append(df_all_sim_data.loc[jj].mean(), ignore_index=True)

    df_median = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.5)
    df_75 = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.75)
    df_25 = quantile_calculate(df_all_sim_data, solver.time_point.__len__(), 0.25)

    fig, axs = plt.subplots(4, 1, figsize=(8, 12))
    index_cov = ['N', 'M', 'B', 'A']
    titles = ["N", "Φ", "β", "α"]
    for kk in range(4):
        # seq_mask = np.isfinite(compare_data[index_cov[kk]])
        # axs[kk].plot(solver.timePoint, df_25.iloc[:, kk], 'b--')
        # axs[kk].plot(solver.timePoint, df_75.iloc[:, kk], 'b--')
        axs[kk].fill_between(solver.time_point, df_25.iloc[:, kk], df_75.iloc[:, kk], alpha=0.9, color='lightgrey')
        axs[kk].plot(solver.time_point, df_mean.iloc[:, kk], 'b', label="Mean", alpha=0.6)
        axs[kk].plot(solver.time_point_default, compare_data[index_cov[kk]], alpha=0.7, marker='^',
                     color='black')
        # axs[kk].errorbar(solver.time_point_exp, compare_data[index_cov[kk]],
        #                  yerr=[[0.5 * x for x in exp_data_SEM[index_cov[kk]]],
        #                        [0.5 * x for x in exp_data_SEM[index_cov[kk]]]], fmt='none',
        #                  ecolor='grey', elinewidth=2, alpha=0.6)
        axs[kk].legend(['Mean', '25% – 75% quantile range', 'Observed'])
        axs[kk].set_title(titles[kk])
    fig.tight_layout(pad=5.0)
    if savefig:
        plt.savefig("resultCurve.png", dpi=200)
    plt.show()
