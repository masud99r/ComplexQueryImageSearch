
def run_evaluation():
    datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    vg_graph_path = datapath+"image2relationship.txt"
    vg_caption_path = datapath+"vg_ms_caption_data.txt"
    vg_graph_map = {}
    with open(vg_graph_path) as f_vggraph:
        for line in f_vggraph:
            vg_id, rel = line.split("\t")
            vg_graph_map[vg_id] = rel
    vg_caption_map = {}
    with open(vg_caption_path) as f_vgcap:
        for line in f_vgcap:
            vg_id, rel = line.split("\t")
            vg_caption_map[vg_id] = rel

    print ("Done")
if __name__ == '__main__':
    run_evaluation()