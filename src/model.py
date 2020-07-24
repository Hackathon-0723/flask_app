import torch
import torchvision
from torch import nn
import numpy as np
import PIL
from torchvision import transforms
from . import consts


class Identity(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x


class MLP(nn.Module):
    # layer_sizes[0] is the dimension of the input
    # layer_sizes[-1] is the dimension of the output
    def __init__(self, layer_sizes, final_relu=False):
        super().__init__()
        layer_list = []
        layer_sizes = [int(x) for x in layer_sizes]
        num_layers = len(layer_sizes) - 1
        final_relu_layer = num_layers if final_relu else num_layers - 1
        for i in range(len(layer_sizes) - 1):
            input_size = layer_sizes[i]
            curr_size = layer_sizes[i + 1]
            if i < final_relu_layer:
                layer_list.append(nn.ReLU(inplace=True))
            layer_list.append(nn.Linear(input_size, curr_size))
        self.net = nn.Sequential(*layer_list)
        self.last_linear = self.net[-1]

    def forward(self, x):
        return self.net(x)


def get_trunk(trunk_model):
    assert trunk_model in ['resnet34'], 'trunk model [{}] is not implemented.'.format(trunk_model)
    if trunk_model == 'resnet34':
        trunk = torchvision.models.resnet34(pretrained=True)
    trunk_output_size = trunk.fc.in_features
    trunk.fc = Identity()
    return trunk, trunk_output_size


class Classifier(nn.Module):
    def __init__(self, trunk_model, layer_sizes, final_relu=False):
        super().__init__()
        self.trunk, trunk_output_size = get_trunk(trunk_model)
        layer_sizes.insert(0, trunk_output_size)
        print(layer_sizes)
        self.embedder = MLP(layer_sizes, final_relu)

    def forward(self, x):
        y = self.embedder(self.trunk(x))
        return y


class MLModel():
    def __init__(self, model_path, threshold=0.8):
        self.net = torch.load(model_path)
        self.threshold = threshold
        self.transform = transforms.Compose([
                        PIL.Image.fromarray,
                        transforms.Resize([224, 224]),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                      ])

    def predict(self, img):
        img = self.transform(img)
        # 1枚ずつ流れてくる場合
        img = img.unsqueeze(0)
        pred = self.net(img)
        pred_idx = np.argmax(pred.detach().cpu().numpy(), axis=1)
        score = pred[0][pred_idx[0]]
        if score > self.threshold:
            pred_label = consts.n2l[pred_idx[0]]
        else:
            pred_label = None
        print('predicted label: ', pred_label)
        return pred_label