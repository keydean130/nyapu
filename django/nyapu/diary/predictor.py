import logging
import os

import math
import torch
import torch.nn as nn
from PIL import Image
from django.conf import settings
from django.core.cache import cache
from torch.nn import functional as F
from torchvision import models
from torchvision import transforms

logger = logging.getLogger(__name__)


class Predictor:
    def __init__(self):
        self.classes = [
            'アビシニアン',
            'アメリカンボブテール',
            'アメリカンショートヘア',
            'ベンガル',
            'バーマン',
            'ムンバイ',
            'ブリティッシュショートヘア',
            'エジプシャンマウ',
            'メインクーン',
            'ペルシアン',
            'ラグドール',
            'ロシアンブルー',
            'シャム',
            'スフィンクス',
            'タキシード'
        ]
        # モデル生成
        cache_key = 'model'
        self.net = cache.get(cache_key)
        if self.net is None:
            logger.info('model is not cached')
            # モデルの作成
            self.net = models.vgg19_bn(pretrained=False)
            # 最終ノードの出力は品種数
            # このノードのみ勾配計算をすることになる
            in_features = self.net.classifier[6].in_features
            self.net.classifier[6] = nn.Linear(in_features, len(self.classes))
            pth_path = 'pretrained/cat_breed_model_cpu.pth'
            self.net.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, pth_path)))
            # 初回にキャッシュして、2回目以降はキャッシュ読み込み
            cache.set(cache_key, self.net, None)
        else:
            logger.info('use cached model')

    def predict(self, diary, k=3):
        logger.info(diary.photo1)
        logger.info(k)
        # 画像の読み込み
        img = Image.open(diary.photo1)
        # transforms関数の定義
        preprocess_img = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(0.5, 0.5)
        ])
        # 正規化
        img_transformed = preprocess_img(img)
        inputs = img_transformed.unsqueeze(0)
        # 推論
        self.net.eval()
        outputs = self.net(inputs)
        batch_probs = F.softmax(outputs, dim=1)
        batch_probs, batch_indices = batch_probs.sort(dim=1, descending=True)
        for probs, indices in zip(batch_probs, batch_indices):
            # 上位3位の推測結果をDBに格納(これ、エラーでえへんけど、DB更新できてない)
            diary.photo1_most_similar_breed = self.classes[indices[0]]
            diary.photo1_second_similar_breed = self.classes[indices[1]]
            diary.photo1_third_similar_breed = self.classes[indices[2]]
            diary.photo1_most_similar_rate = math.ceil(probs[0] * 100)
            diary.photo1_second_similar_rate = math.ceil(probs[1] * 100)
            diary.photo1_third_similar_rate = math.ceil(probs[2] * 100)
        return diary
