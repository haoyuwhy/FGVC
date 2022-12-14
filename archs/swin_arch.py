from turtle import forward
import torch
from typing import Union
from .pim_module import PluginMoodel
import torch.nn as nn
from basicsr.utils.registry import ARCH_REGISTRY



def build_swintransformer(pretrained: bool = True,
                          num_selects: Union[dict, None] = None, 
                          img_size: int = 384,
                          use_fpn: bool = True,
                          fpn_size: int = 512,
                          proj_type: str = "Linear",
                          upsample_type: str = "Conv",
                          use_selection: bool = True,
                          num_classes: int = 200,
                          use_combiner: bool = True,
                          comb_proj_size: Union[int, None] = None,
                          **kwargs):
    """
    This function is to building swin transformer. timm swin-transformer + torch.fx.proxy.Proxy 
    could cause error, so we set return_nodes to None and change swin-transformer model script to
    return features directly.
    Please check 'timm/models/swin_transformer.py' line 541 to see how to change model if your costom
    model also fail at create_feature_extractor or get_graph_node_names step.
    """

    import timm

    if num_selects is None:
        num_selects = {
            'layer1':2048,
            'layer2':512,
            'layer3':128,
            'layer4':32
        }

    backbone = timm.create_model('swin_large_patch4_window12_384_in22k', pretrained=pretrained,**kwargs)

    # print(backbone)
    # print(get_graph_node_names(backbone))
    backbone.train()
    
    print("Building...")
    return PluginMoodel(backbone = backbone,
                                   return_nodes = None,
                                   img_size = img_size,
                                   use_fpn = use_fpn,
                                   fpn_size = fpn_size,
                                   proj_type = proj_type,
                                   upsample_type = upsample_type,
                                   use_selection = use_selection,
                                   num_classes = num_classes,
                                   num_selects = num_selects, 
                                   use_combiner = num_selects,
                                   comb_proj_size = comb_proj_size)

@ARCH_REGISTRY.register()
class SwinTransfomer(nn.Module):
    def __init__(self,pretrain=False,lables=200,**kwargs) -> None:
        super(SwinTransfomer,self).__init__()
        self.net=build_swintransformer(pretrain,num_classes=lables,**kwargs)
    
    def forward(self,x):
        return self.net(x)

    
