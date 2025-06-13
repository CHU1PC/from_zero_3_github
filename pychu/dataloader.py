import math

import numpy as np
from pychu import cuda


class DataLoader:
    def __init__(self, dataset, batch_size, shuffle=True, gpu=False):
        """datasetを受取りbatch_sizeに対してiterを作る

        Args:
            dataset (Dataset): Datasetのインスタンス
            batch_size (int): 1回のイテレーションで取得するデータ数
            shuffle (bool): データをシャッフルして取得するかどうか.デフォルトはTrue
        """
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.data_size = len(dataset)
        self.max_iter = math.ceil(self.data_size / batch_size)
        self.gpu = gpu

        self.reset()

    def reset(self):
        """
        インスタンス変数のiterationを0にリセットする
        """
        self.iteration = 0
        if self.shuffle:
            self.index = np.random.permutation(len(self.dataset))
        else:
            self.index = np.arange(len(self.dataset))

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteration >= self.max_iter:
            self.reset()
            raise StopIteration

        i, batchsize = self.iteration, self.batch_size
        batch_index = self.index[i * batchsize:(i + 1) * batchsize]
        batch = [self.dataset[i] for i in batch_index]
        xp = cuda.cupy if self.gpu else np
        x = xp.array([example[0] for example in batch])
        t = xp.array([example[1] for example in batch])

        self.iteration += 1
        return x, t

    def next(self):
        return self.__next__()

    def to_cpu(self):
        self.gpu = False

    def to_gpu(self):
        self.gpu = True
