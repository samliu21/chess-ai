# chess-ai

Here's a video where I (white) get crushed by my bot (black) :)

https://user-images.githubusercontent.com/64169932/152080181-d7370b95-b44e-4d91-aa54-a69f4d3d5795.mov

## Playing against the AI!
1. Run `git clone https://github.com/samliu21/chess-ai`. Navigate into the directory with `cd chess-ai`.
2. Create a virtual environment using `python -m venv .` and activate it with `source bin/activate`.
3. Install the necessary dependencies using `python -m pip install -r requirements.txt`.
4. Call `python gui/main.py` to play!

## GUI
The GUI was hand-made using the `pygame` and `python-chess` modules.

## AI Architecture
This architecture was largely inspired by this <a href="http://cs231n.stanford.edu/reports/2015/pdfs/ConvChess.pdf">Standford paper</a>.

The AI uses two models. They both receive a board position as input and output an `8x8` matrix of softmax probabilities. The "from model" predicts the square to be moved out of and the "to model" predicts the square to be moved into.

The approach is best illustrated with an example. Consider the starting board position and the move: `Nf3`. The evaluation of this move is the product of the value at the `g1` square of the from model and the value at the `f3` square of the to model.

Among all legal moves, the largest product is the selected move. 

The neural networks consist of five convolutional layers, followed by two affine layers and an output layer. A more detailed sketch of the architecture can be found below:

```
Model: "model"
__________________________________________________________________________________________________
 Layer (type)                   Output Shape         Param #     Connected to                     
==================================================================================================
 input_1 (InputLayer)           [(None, 8, 8, 12)]   0           []                               
                                                                                                  
 conv2d (Conv2D)                (None, 8, 8, 32)     3488        ['input_1[0][0]']                
                                                                                                  
 batch_normalization (BatchNorm  (None, 8, 8, 32)    128         ['conv2d[0][0]']                 
 alization)                                                                                       
                                                                                                  
 activation (Activation)        (None, 8, 8, 32)     0           ['batch_normalization[0][0]']    
                                                                                                  
 conv2d_1 (Conv2D)              (None, 8, 8, 64)     18496       ['activation[0][0]']             
                                                                                                  
 batch_normalization_1 (BatchNo  (None, 8, 8, 64)    256         ['conv2d_1[0][0]']               
 rmalization)                                                                                     
                                                                                                  
 activation_1 (Activation)      (None, 8, 8, 64)     0           ['batch_normalization_1[0][0]']  
                                                                                                  
 conv2d_2 (Conv2D)              (None, 8, 8, 256)    147712      ['activation_1[0][0]']           
                                                                                                  
 batch_normalization_2 (BatchNo  (None, 8, 8, 256)   1024        ['conv2d_2[0][0]']               
 rmalization)                                                                                     
                                                                                                  
 activation_2 (Activation)      (None, 8, 8, 256)    0           ['batch_normalization_2[0][0]']  
                                                                                                  
 concatenate (Concatenate)      (None, 8, 8, 512)    0           ['activation_2[0][0]',           
                                                                  'activation_2[0][0]']           
                                                                                                  
 conv2d_3 (Conv2D)              (None, 8, 8, 256)    1179904     ['concatenate[0][0]']            
                                                                                                  
 batch_normalization_3 (BatchNo  (None, 8, 8, 256)   1024        ['conv2d_3[0][0]']               
 rmalization)                                                                                     
                                                                                                  
 activation_3 (Activation)      (None, 8, 8, 256)    0           ['batch_normalization_3[0][0]']  
                                                                                                  
 concatenate_1 (Concatenate)    (None, 8, 8, 320)    0           ['activation_3[0][0]',           
                                                                  'activation_1[0][0]']           
                                                                                                  
 conv2d_4 (Conv2D)              (None, 8, 8, 256)    737536      ['concatenate_1[0][0]']          
                                                                                                  
 batch_normalization_4 (BatchNo  (None, 8, 8, 256)   1024        ['conv2d_4[0][0]']               
 rmalization)                                                                                     
                                                                                                  
 activation_4 (Activation)      (None, 8, 8, 256)    0           ['batch_normalization_4[0][0]']  
                                                                                                  
 concatenate_2 (Concatenate)    (None, 8, 8, 288)    0           ['activation_4[0][0]',           
                                                                  'activation[0][0]']             
                                                                                                  
 conv2d_5 (Conv2D)              (None, 8, 8, 256)    663808      ['concatenate_2[0][0]']          
                                                                                                  
 batch_normalization_5 (BatchNo  (None, 8, 8, 256)   1024        ['conv2d_5[0][0]']               
 rmalization)                                                                                     
                                                                                                  
 activation_5 (Activation)      (None, 8, 8, 256)    0           ['batch_normalization_5[0][0]']  
                                                                                                  
 dense (Dense)                  (None, 8, 8, 256)    65792       ['activation_5[0][0]']           
                                                                                                  
 batch_normalization_6 (BatchNo  (None, 8, 8, 256)   1024        ['dense[0][0]']                  
 rmalization)                                                                                     
                                                                                                  
 dense_1 (Dense)                (None, 8, 8, 64)     16448       ['batch_normalization_6[0][0]']  
                                                                                                  
 batch_normalization_7 (BatchNo  (None, 8, 8, 64)    256         ['dense_1[0][0]']                
 rmalization)                                                                                     
                                                                                                  
 dense_2 (Dense)                (None, 8, 8, 1)      65          ['batch_normalization_7[0][0]']  
                                                                                                  
 batch_normalization_8 (BatchNo  (None, 8, 8, 1)     4           ['dense_2[0][0]']                
 rmalization)                                                                                     
                                                                                                  
 softmax (Softmax)              (None, 8, 8, 1)      0           ['batch_normalization_8[0][0]']  
                                                                                                  
==================================================================================================
Total params: 2,839,013
Trainable params: 2,836,131
Non-trainable params: 2,882
__________________________________________________________________________________________________
```

## Failed Attempt
The initial approach was to use machine learning to create a board evaluation neural network. Combined with a minimax algorithm with alpha-beta pruning, the hope was that this algorithm would create a strong chess AI. There were two issues with this approach:

1. The evaluation network didn't perform to my expectations. It could detect material imbalances but couldn't detect simple checkmates.

2. Due to the large action space of chess, minimax is very slow, even when optimzied with alpha-beta pruning.

Together, these factors prompted me to scrap this initial idea and try another.