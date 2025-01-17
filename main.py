from __future__ import print_function

import argparse

from torch.utils.data import DataLoader

from SRCNN.solver import SRCNNTrainer
from FSRCNN.solver import FSRCNNTrainer
from SubPixelCNN.solver import SubPixelTrainer
from VDSR.solver import VDSRTrainer
from DRCN.solver import DRCNTrainer
from SRGAN.solver import SRGANTrainer
from EDSR.solver import EDSRTrainer
from DBPN.solver import DBPNTrainer
from dataset.data import get_training_set, get_test_set

# ===========================================================
# Training settings
# ===========================================================
parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
# hyper-parameters
parser.add_argument('--batchSize', type=int, default=4, help='training batch size')
parser.add_argument('--testBatchSize', type=int, default=2, help='testing batch size')
parser.add_argument('--nEpochs', type=int, default=20, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.002, help='Learning Rate. Default=0.01')
parser.add_argument('--seed', type=int, default=123, help='random seed to use. Default=123')

# model configuration
parser.add_argument('--upscale_factor', '-uf',  type=int, default=4, help="super resolution upscale factor")
parser.add_argument('--model', '-m', type=str, default='srgan',
                    choices=['srcnn', 'fsrcnn', 'sub', 'vdsr', 'drcn', 'srgan', 'edsr', 'dbpn'], help='choose which model is going to use')
args = parser.parse_args()

# %%
def main():
    # ===========================================================
    # Set train dataset & test dataset
    # ===========================================================
    print('===> Loading datasets')
    train_set = get_training_set(args.upscale_factor)
    test_set = get_test_set(args.upscale_factor)
    training_data_loader = DataLoader(dataset=train_set, batch_size=args.batchSize, shuffle=True)
    testing_data_loader = DataLoader(dataset=test_set, batch_size=args.testBatchSize, shuffle=False)

    if args.model == 'sub':
        model = SubPixelTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'srcnn':
        model = SRCNNTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'vdsr':
        model = VDSRTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'edsr':
        model = EDSRTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'fsrcnn':
        model = FSRCNNTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'drcn':
        model = DRCNTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'srgan':
        model = SRGANTrainer(args, training_data_loader, testing_data_loader)
    elif args.model == 'dbpn':
        model = DBPNTrainer(args, training_data_loader, testing_data_loader)
    else:
        raise Exception("the model does not exist")

    model.run()


if __name__ == '__main__':
    main()

# %%
