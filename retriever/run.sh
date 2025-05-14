# datastore_raw_data_path=/future/u/gharshit/lotus-research/data/peS2o  # directory that contains the converted jsonl data
# num_shards=16

# # Run indexing tasks in parallel
# for TASK_ID in {8..15}; do 
# PYTHONPATH=.  python ric/main_ric.py \
#   --config-name=pes2o_v3 \
#   tasks.datastore.embedding=false \
#   tasks.datastore.index=true \
#   datastore.raw_data_path=$datastore_raw_data_path \
#   datastore.embedding.num_shards=$num_shards \
#   datastore.embedding.shard_ids=[$TASK_ID] \
#   datastore.index.index_shard_ids=[$TASK_ID] \
#   hydra.job_logging.handlers.file.filename=embedding_${TASK_ID}.log
# done



EVAL_DOMAIN=pes2o_v3
RAW_QUERY=/future/u/gharshit/lotus-research/data/papers.jsonl
EVAL_OUTPUT_DIR=/future/u/gharshit/lotus-research/data/retrieved_papers

DS_NAME=pes2o_v3
NUM_SHARDS=16
N_DOCS=100

index_list="[[0]"
for (( i=1; i<=$((NUM_SHARDS - 1)); i++ )); do
index_list+=",[$i]"
done
index_list+="]"
echo INDEX_IDS:$index_list

PYTHONPATH=.  python ric/main_ric.py \
    --config-name pes2o_v3 \
    tasks.eval.task_name=lm-eval \
    tasks.eval.search=true \
    datastore.embedding.num_shards=$NUM_SHARDS \
    datastore.embedding.shard_ids=[] \
    datastore.index.index_shard_ids=$index_list \
    evaluation.domain=$EVAL_DOMAIN \
    evaluation.data.eval_data=$RAW_QUERY \
    evaluation.search.n_docs=$N_DOCS \
    evaluation.eval_output_dir=$EVAL_OUTPUT_DIR # where the retrieved documents will be saved