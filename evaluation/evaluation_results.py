import operator
import search.similarities.bm25.okapi_bm25 as model_bm25
def keyword_based_graph_similarity(graph1, graph2):
    graph1_parts = remove_string_noise(str(graph1)).split(" ")
    graph2_parts = remove_string_noise(str(graph2)).split(" ")
    #keyword matching
    match_count = 0
    for relation1 in graph1_parts:
        for relation2 in graph2_parts:
            if relation1 == relation2:
                match_count += 1
    return match_count
def remove_string_noise(input_str):
    #give special char you want to remove
    #do not put space between chars, and space (" ") is not a special char
    punctuation_noise ="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" #print string.punctuation
    number_noise = "0123456789"
    special_noise = ""

    all_noise = punctuation_noise + number_noise + special_noise

    for c in all_noise:
        if c in input_str:
            input_str = input_str.replace(c, " ")#replace with space
    input_str = input_str.replace("NONE","")
    fresh_str = ' '.join(input_str.split())
    return fresh_str
def run_evaluation():
    #datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    vg_graph_path = datapath+"candidate_document.txt"
    vg_caption_path = datapath+"query.txt"

    querycaption = {}
    vg_graph_map = {}
    with open(vg_graph_path) as f_vggraph:
        for line in f_vggraph:
            vg_id, rel = line.split("\t")
            vg_id = int(vg_id)
            vg_graph_map[vg_id] = rel
    vg_caption_map = {}
    with open(vg_caption_path) as f_vgcap:
        for line in f_vgcap:
            vg_id, caption, rel = line.split("\t")
            vg_id = int(vg_id)
            querycaption[vg_id] = caption
            vg_caption_map[vg_id] = rel
    query_count = 0
    total_mrr = 0.0
    total_query = 20
    '''
    for query in vg_caption_map:
        query_count += 1
        if query in vg_graph_map:
            score_map = {}
            query_graph = vg_caption_map[query]
            for candidate in vg_caption_map:
                if candidate in vg_graph_map:
                    candidate_graph = vg_graph_map[candidate]#consider candidate scene graph only
                    score = keyword_based_graph_similarity(query_graph, candidate_graph)
                    score_map[candidate] = score
            sorted_scores_list = sorted(score_map.items(), key=operator.itemgetter(1), reverse=True)  # large value means more similar
            print ("Query = "+str(query)+"\t"+str(querycaption[query])+"\t"+"https://cs.stanford.edu/people/rak248/VG_100K/"+str(query)+".jpg")
            topcount = 0
            query_mrr = 0
            for score_tuple in sorted_scores_list:
                topcount += 1
                candidate_id, score_value = score_tuple
                if candidate_id == query:#this will happen at most once
                    rank = topcount
                    print ("Rank is = "+str(rank))
                    query_mrr = 1.0/int(rank)
                if topcount < 10:
                    print (str(score_tuple)+"\t"+"https://cs.stanford.edu/people/rak248/VG_100K/"+str(candidate_id)+".jpg")
            total_mrr += query_mrr
        else:
            print ("Not found in VG")
        if query_count>total_query:
            averageMRR = total_mrr/total_query
            print ("avg MRR = "+str(averageMRR))
            break
        '''
    search_results_score, search_results_sorted = model_bm25.generate_results(datapath, "2365441")
    print search_results_sorted

    print ("Done")

def run_evaluation_v2():
    #datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    vg_graph_path = datapath+"candidate_document.txt"
    vg_caption_path = datapath+"query_document.txt"

    candidate_list = []
    query_map = {}
    querycaption = {}
    id_list = []
    with open(vg_graph_path) as f_vggraph:
        for line in f_vggraph:
            candidate_list.append(line)
    vg_caption_map = {}
    with open(vg_caption_path) as f_vgcap:
        for line in f_vgcap:
            vg_id, caption, rel = line.split("\t")
            vg_id = int(vg_id)
            id_list.append(vg_id)
            querycaption[vg_id] = caption
            vg_caption_map[vg_id] = rel
    query_count = 0
    total_mrr = 0.0
    total_query = 200
    rank_list = []
    for query_id in vg_caption_map:

        search_results_score, search_results_sorted = model_bm25.generate_results(datapath,str(query_id))
        #print ("Query = " + str(query_id) + "\t" + str(
            #querycaption[query_id]) + "\t" + "https://cs.stanford.edu/people/rak248/VG_100K/" + str(query_id) + ".jpg"+ "\t" + "Alternative: https://cs.stanford.edu/people/rak248/VG_100K_2/" + str(query_id) + ".jpg")
        topcount = 0
        query_mrr = 0
        for score_tuple in search_results_sorted[0]:
            topcount += 1
            candidate_index, score_value = score_tuple
            candidate_id = id_list[candidate_index]
            if candidate_id == query_id:  # this will happen at most once
                rank = topcount
                rank_list.append(rank)
                #print ("Rank is = " + str(rank))
                query_mrr = 1.0 / int(rank)
            #if topcount < 10:
                #print (
                #str(score_tuple) + "\t" + "https://cs.stanford.edu/people/rak248/VG_100K/" + str(candidate_id) + ".jpg"+ "\t" + "Alternative: https://cs.stanford.edu/people/rak248/VG_100K_2/" + str(candidate_id) + ".jpg")
        total_mrr += query_mrr
        query_count += 1
        print query_count
        if query_count > total_query:
            averageMRR = total_mrr / query_count
            print ("avg MRR = " + str(averageMRR))
            print rank_list
            top1_count = 0
            top5_count = 0
            top10_count = 0
            top15_count = 0
            top20_count = 0
            for rank_val in rank_list:
                if rank_val <= 1:
                    top1_count += 1
                if rank_val <= 5:
                    top5_count += 1
                if rank_val <= 10:
                    top10_count += 1
                if rank_val <= 15:
                    top15_count += 1
                if rank_val <= 20:
                    top20_count += 1
            recall_1 = (top1_count*1.0)/total_query
            recall_5 = (top5_count*1.0)/total_query
            recall_10 = (top10_count*1.0)/total_query
            recall_15 = (top15_count*1.0)/total_query
            recall_20 = (top20_count*1.0)/total_query
            sorted_rank_list = sorted(rank_list)
            print sorted_rank_list
            midindex = len(sorted_rank_list)/2
            print ("Median Rank = "+str(sorted_rank_list[midindex]))
            print ("Recall\t"+str(recall_1)+"\t"+str(recall_5)+"\t"+str(recall_10)+"\t"+str(recall_15)+"\t"+str(recall_20))
            break


    print ("Done")
if __name__ == '__main__':
    #run_evaluation()
    run_evaluation_v2()