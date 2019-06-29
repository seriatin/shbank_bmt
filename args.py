import argparse

def bmt_args():
    parser = argparse.ArgumentParser(description="ShinHan Bank Model Training BMT")
    parser.add_argument('--data_dir', type=str, default='.', help='MNIST Pickle Data Directory')
    parser.add_argument('--epochs', type=int, default=10, help='Training Epochs or Step')
    parser.add_argument('--model_name', type=str, default='mnist', help='Saved Model Name')
    parser.add_argument('--export_dir', type=str, default='./freeze', help='Export Serving Model')
    parser.add_argument('--checkpoint_dir', type=str, default='./checkpoint', help='Save Model Checkpoint')

    return parser
