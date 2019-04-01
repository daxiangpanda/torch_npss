import hparams
from model.wavenet_model import *
from data.dataset import TimbreDataset
from model.timbre_training import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = WaveNetModel(hparams.create_harmonic_hparams(), device).to(device)
print('model: ', model)
print('receptive field: ', model.receptive_field)
print('parameter count: ', model.parameter_count())
data = TimbreDataset(data_folder='data/timbre_model', receptive_field=model.receptive_field, type=0)
print('the dataset has ' + str(len(data)) + ' items')
trainer = ModelTrainer(model=model,
                       dataset=data,
                       lr=0.0005,
                       weight_decay=0.0,
                       snapshot_path='./snapshots/harmonic',
                       snapshot_name='chaconne_model',
                       snapshot_interval=2000,
                       device=device,
                       temperature=0.05)


def exit_handler():
    trainer.save_model()
    print("exit from keyboard")


#atexit.register(exit_handler)

#epoch = trainer.load_checkpoint('snapshots/harmonic/chaconne_model_1649_2019-03-28_23-00-34')

print('start training...')
trainer.train(batch_size=128,
              epochs=1650)