#!/bin/sh

model_name=Timer
seq_len=672
label_len=576
pred_len=96
output_len=96
patch_len=96
ckpt_path=checkpoints/Timer_forecast_1.0.ckpt
data=ETTh1

# for subset_rand_ratio in 0.01 0.02 0.03 0.04 0.05 0.1 0.15 0.2 0.25 0.5 0.75 1
# do
# # train
# torchrun --nnodes=1 --nproc_per_node=4 run.py \
#   --task_name forecast \
#   --is_training 0 \
#   --seed 1 \
#   --ckpt_path $ckpt_path \
#   --root_path ./dataset/ETT-small/ \
#   --data_path $data.csv \
#   --data $data \
#   --model_id etth1_sr_$subset_rand_ratio \
#   --model $model_name \
#   --features M \
#   --seq_len $seq_len \
#   --label_len $label_len \
#   --pred_len $pred_len \
#   --output_len $output_len \
#   --e_layers 8 \
#   --factor 3 \
#   --des 'Exp' \
#   --d_model 1024 \
#   --d_ff 2048 \
#   --batch_size 2048 \
#   --learning_rate 3e-5 \
#   --num_workers 4 \
#   --patch_len $patch_len \
#   --train_test 0 \
#   --subset_rand_ratio $subset_rand_ratio \
#   --itr 1 \
#   --gpu 0 \
#   --use_ims \
#   --use_multi_gpu
# done


python -u run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 32 --learning_rate 3e-5 --num_workers 2 --patch_len 96 --train_test 0 --subset_rand_ratio 0.01 --itr 1 --gpu 0 --use_ims 

# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.01 --itr 1 --gpu 0 --use_ims 
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.02 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.03 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.04 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.05 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.10 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.15 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.20 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.25 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.50 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 0.75 --itr 1 --gpu 0 --use_ims --use_multi_gpu
# torchrun --nnodes=1 --nproc_per_node=4 run.py --task_name forecast --is_training 0 --seed 1 --ckpt_path checkpoints/Timer_forecast_1.0.ckpt --root_path ./dataset/ETT-small/ --data_path ETTh1.csv --data ETTh1 --model_id etth1_sr_0.01 --model Timer --features M --seq_len 672 --label_len 576 --pred_len 96 --output_len 96 --e_layers 8 --factor 3 --des 'Exp' --d_model 1024 --d_ff 2048 --batch_size 2048 --learning_rate 3e-5 --num_workers 4 --patch_len 96 --train_test 0 --subset_rand_ratio 1.0 --itr 1 --gpu 0 --use_ims --use_multi_gpu