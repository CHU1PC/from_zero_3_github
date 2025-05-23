import unittest

import numpy as np
from step9 import Variable, square


class SquareTest(unittest.TestCase):
    def test_forward(self):
        x = Variable(np.array(2.0))
        y = square(x)
        expected = np.array(4.0)
        self.assertEqual(y.data, expected)

    def test_backward(self):
        x = Variable(np.array(np.array(3.0)))
        y = square(x)
        y.backward()
        expected = np.array(6.0)
        self.assertEqual(x.grad, expected)

    def test_gradient_check(self):
        # ランダムな値でしっかりと微分できているかを判断する
        x = Variable(np.random.rand(1))

        y = square(x)

        # バックプロパゲーションと数値微分を使ってもとめる
        y.backward()
        num_grad = numerical_diff(square, x)

        # 値が近いかどうかをTrue, Falseで返す
        flg = np.allclose(x.grad, num_grad)  # type: ignore
        self.assertTrue(flg)


def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)

    return (y1.data - y0.data) / (2 * eps)


unittest.main()
