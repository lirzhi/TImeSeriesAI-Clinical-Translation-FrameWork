# model_name=Timer
# seq_len=672
# label_len=576
# pred_len=96
# output_len=96
# patch_len=96
# ckpt_path=checkpoints/Timer_forecast_1.0.ckpt
# data=illness

# python -u run.py --task_name forecast --is_training 1 --root_path ./dataset/illness/ --data_path illness.csv --model_id ili_36_24 --model Timer --data custom --features M --seq_len 36 --label_len 18 --pred_len 24 --e_layers 2 --d_layers 1 --factor 3 --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
# python -u run.py --task_name forecast --is_training 1 --root_path ./dataset/illness/ --data_path illness.csv --model_id ili_36_36 --model Timer --data custom --features M --seq_len 36 --label_len 18 --pred_len 36 --e_layers 2 --d_layers 1 --factor 3 --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
# python -u run.py --task_name forecast --is_training 1 --root_path ./dataset/illness/ --data_path illness.csv --model_id ili_36_48 --model Timer --data custom --features M --seq_len 36 --label_len 18 --pred_len 48 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
export CUDA_VISIBLE_DEVICES=""

model_name=iTransformer
# 默认参数
root_path="./dataset/illness/"
data_path="illness.csv"
is_training=0
is_finetuning=0
python -u run.py --task_name forecast --is_finetuning $is_finetuning --is_training $is_training --root_path $root_path --data_path $data_path --model_id ili_36_72 --model Timer --data custom --features M --seq_len 96 --label_len 18 --pred_len 24 --output_len 24 --patch_len 12 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
python -u run.py --task_name forecast --is_finetuning $is_finetuning --is_training $is_training --root_path $root_path --data_path $data_path --model_id ili_36_72 --model Timer --data custom --features M --seq_len 96 --label_len 18 --pred_len 36 --output_len 36 --patch_len 12 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
python -u run.py --task_name forecast --is_finetuning $is_finetuning --is_training $is_training --root_path $root_path --data_path $data_path --model_id ili_36_72 --model Timer --data custom --features M --seq_len 96 --label_len 18 --pred_len 48 --output_len 48  --patch_len 12 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
python -u run.py --task_name forecast --is_finetuning $is_finetuning --is_training $is_training --root_path $root_path --data_path $data_path --model_id ili_36_72 --model Timer --data custom --features M --seq_len 96 --label_len 18 --pred_len 60 --output_len 60 --patch_len 12 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False
python -u run.py --task_name forecast --is_finetuning $is_finetuning --is_training $is_training --root_path $root_path --data_path $data_path --model_id ili_36_72 --model Timer --data custom --features M --seq_len 96 --label_len 18 --pred_len 72 --output_len 72 --patch_len 12 --e_layers 2 --d_layers 1 --factor 3  --des 'Exp' --itr 1 --target OT --freq w --checkpoints ./checkpoints/ --num_workers 4 --train_epochs 10 --batch_size 32 --patience 3 --learning_rate 3e-5 --loss MSE --use_gpu False

# torchrun --nnodes=1 --nproc_per_node=4 run.py \
#   --task_name forecast \
#   --is_training 0 \
#   --ckpt_path $ckpt_path \
#   --seed 1 \
#   --root_path ./dataset/$data/ \
#   --data_path $data.csv \
#   --data custom \
#   --model_id traffic_sr_$subset_rand_ratio \
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