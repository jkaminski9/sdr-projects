import numpy as np
from scipy.io import wavfile
import os
from scipy.stats import kurtosis, skew
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score as acc
from python_speech_features import mfcc
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import pickle

def generate_stats(signal):
    return np.array([np.var(signal), skew(signal), kurtosis(signal)])

def generate_features_labels(raw_data, num_files, rx_rate, sample_len_seconds):
    first = True
    sample_len_samples = sample_len_seconds*rx_rate
    labels = []
    file_num = 0
    for genre in list(raw_data.keys()):
        signals = raw_data[genre]
        for signal in signals:
            mfcc_feat = mfcc(signal, rx_rate, winlen=0.020, appendEnergy = False)
            covariance = np.cov(np.matrix.transpose(mfcc_feat))
            mean_matrix = mfcc_feat.mean(0)
            skew_matrix = skew(mfcc_feat, axis=0)
            kurtosis_matrix = kurtosis(mfcc_feat, axis=0)
            feat = np.concatenate((mean_matrix, covariance.flatten(), skew_matrix, kurtosis_matrix))
            if first:
                features = feat.reshape([1, len(feat)])
                first = False
            else:
                feat = feat.reshape([1, len(feat)])
                features = np.append(features, feat, axis=0)
            file_num += 1
            print(file_num)
            labels.append(genre)
    return features, labels


if __name__ == "__main__":
    load_data = True
    segment_length_seconds = 30
    genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

    if load_data:
        dataset_dir = "gtzan_dataset"
        raw_data = {}
        num_files = 0
        for genre in genres:
            path = os.path.join(dataset_dir, genre)
            first_file = True
            data_list = []
            for file in os.listdir(path):
                if ".wav" in file:
                    try:
                        sample_rate, data = wavfile.read(os.path.join(path,file))
                        data = data.astype(np.float32)
                        data = (data - data.min()) / (data.max() - data.min())
                        segment_length_samples = segment_length_seconds * sample_rate
                        num_segments = int(len(data) / segment_length_samples)
                        for i in range(num_segments):
                            data_list.append(data[i*segment_length_samples:(i*segment_length_samples)+segment_length_samples])
                        num_files += 1
                    except:
                        print("Skipping File: " + file)
            raw_data[genre] = data_list


        features, labels = generate_features_labels(raw_data, num_files, sample_rate, 3)

        np.save("Features.npy", features)
        np.save("Labels.npy", np.array(labels))

    else:
        features = np.load("Features.npy")
        labels = np.load("Labels.npy")

    print(features.shape)
    scaler = StandardScaler().fit(features)
    features = scaler.transform(features)

    lda = LDA().fit(features, labels)

    features_lda = lda.transform(features)

    pca = PCA(n_components=2).fit(features_lda)
    features_pca = pca.transform(features_lda)

    labels = np.array(labels)

    for genre in genres:
        plt.scatter(features_pca[labels==genre, 0], features_pca[labels==genre, 1], label=genre)

    plt.legend()
    plt.show()

    
    clf = GaussianNB()

    clf.fit(features_lda, labels)
    print(features_lda.dtype)
    print(acc(clf.predict(features_lda), labels))
    labels_pred = clf.predict(features_lda)
    print(labels_pred[0:100], labels[0:10])
    pickle.dump(clf, open("genre_clf.sav", 'wb'))
    pickle.dump(lda, open("genre_lda.sav", 'wb'))
    pickle.dump(scaler, open("genre_scaler.sav", 'wb'))
