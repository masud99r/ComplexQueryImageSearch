import random, json, string
def generate_scene_graph_data(jsonpath):
    attributes_map = {}
    vg_attributes = json.load(open(jsonpath + "/attributes.json"))
    for entry in vg_attributes:
        for attr in entry['attributes']:
            objectid = attr['object_id']
            #print objectid
            objectname = attr['names']
            #print objectname
            try:
                objectattr_list = attr['attributes']
            except:
                objectattr_list = []
                objectattr_list.append("NONE")#no attribute for this objects
            #print objectattr_list
            attributes_map[(str(entry['image_id']) + "_" + str(objectid)).replace("\n","")] = objectattr_list#single tab error!!!!!
        #print (str(entry['image_id']) + "_" + str(objectid))


    vsgid2mscocoid = {}
    vg = json.load(open(jsonpath+"/vg_image_data.json"))
    for entry in vg:
        #print (enrtry['image_id'], enrtry['coco_id'])
        if entry['coco_id'] != None:
            #print (enrtry['image_id'], enrtry['coco_id'])
            vsgid2mscocoid[entry['image_id']] = entry['coco_id']
    #print (vsgid2mscocoid)
    print len(vsgid2mscocoid)
    #captionStrings = [entry['caption'].encode('ascii') for entry in mscoco['annotations']]
    #mscoco_imageid = [entry['image_id'] for entry in mscoco['annotations']]
    relations_map = {}
    vg_relations = json.load(open(jsonpath+"/relationships.json"))
    for entry in vg_relations:
        relations_map[entry['image_id']] = entry
        '''
        print ("=================================")
        print entry['image_id']
        print entry['relationships']
        for rel in entry['relationships']:
            print rel['predicate']
            print rel['object']
            print rel['subject']
        '''

    f_im2rel = open("image2relationship.txt","w")
    print ("Id missmatch check ================================================")
    for image_id in relations_map:
        #if image_id in attributes_map: #extra caution, it should map always with consistent data
        if image_id in vsgid2mscocoid: #filtered not in coco
            relation_entry = relations_map[image_id]
            all_rel = ""
            for rel in relation_entry['relationships']:
                relation_type =  rel['predicate']
                subject_details =  rel['subject']
                subject_objectid = subject_details['object_id']
                subject_name = subject_details['name']
                try:
                    #print (str(image_id)+"_"+str(subject_objectid))
                    subject_attribute_list = attributes_map[(str(image_id)+"_"+str(subject_objectid)).replace("\n","")]
                except:
                    subject_attribute_list = []
                object_details =  rel['object']
                object_objectid = object_details['object_id']
                object_name = object_details['name']
                try:
                    object_attribute_list = attributes_map[str(image_id) + "_" + str(object_objectid)]
                except:
                    object_attribute_list = []


                for subj_attr in subject_attribute_list:
                    for obj_attr in object_attribute_list:
                        processed_entry = str(subj_attr)+"-"+subject_name+":"+str(relation_type)+":"+str(obj_attr)+"-"+object_name
                        all_rel = all_rel+","+processed_entry
            all_rel = all_rel.strip(",")
            f_im2rel.write(str(image_id)+"\t"+all_rel+"\n")
def remove_after_dash(token):
    return str(token).split("-")[0]
def process_caption_data(datapath):
    f_processed = open("vg_caption_relation_attribute_processed.txt","w")
    with open(datapath+"/vg_caption_relation_attribute.txt") as fcap:
        for line in fcap:
            lineParts = line.split("\t")
            vg_id = lineParts[0]
            vg_caption = lineParts[1]
            parser_rel = lineParts[2]
            parser_attribute = lineParts[3]

            #attribute
            obj2attr = {}
            attributesParts = parser_attribute.split(",")
            for entry in attributesParts:
                if (str(entry) == "NONE"):
                    continue
                object, attr = entry.split(":")
                if object in obj2attr:
                    atrr_list = obj2attr[object]
                    atrr_list.append(attr)
                    obj2attr[object] = attr_list
                else:
                    attr_list = []
                    attr_list.append("NONE")
                    attr_list.append(attr)
                    obj2attr[object] = attr_list
            #relationship
            relationParts = parser_rel.split(",")
            processed_relation = ""
            for entry in relationParts:
                if (str(entry)=="NONE"):
                    continue
                entryParts = entry.split(" ")
                subject = entryParts[0]
                object = entryParts[len(entryParts)-1]

                relation = entryParts[1]
                for i in range(2,len(entryParts)-1):
                    relation = relation+" "+entryParts[i]

                #relation_item = "NONE-" + str(remove_after_dash(subject))+":"+relation+":"+"NONE-" +str(remove_after_dash(object))
                #processed_relation = processed_relation+","+relation_item

                rel_list_subject = []
                rel_list_subject.append("NONE")
                if subject in obj2attr:
                    rel_list_subject = obj2attr[subject]#if exist replace with the actual attribute
                rel_list_object = []
                rel_list_object.append("NONE")
                if object in obj2attr:
                    rel_list_object = obj2attr[object]  # if exist replace with the actual attribute

                for subj_attr in rel_list_subject:
                    for obj_attr in rel_list_object:
                        relation_item = str(subj_attr) + "-" + remove_after_dash(subject) + ":" + str(relation) + ":" + str(obj_attr) + "-" + remove_after_dash(object)
                        processed_relation = processed_relation + "," + relation_item
            processed_relation = processed_relation.strip(",")
            f_processed.write(str(vg_id) + "\t" + str(vg_caption) + "\t"+processed_relation+"\n")

    f_processed.close()
def data_filter():
    datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    #datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    vg_graph_path = datapath + "image2relationship.txt"
    vg_caption_path = datapath + "vg_caption_relation_attribute_processed.txt"

    f_graph = open(datapath + "image2relationship_filtered.txt","w")
    f_cap = open(datapath + "vg_caption_relation_attribute_processed_filtered.txt","w")

    vg_graph_map = {}
    with open(vg_graph_path) as f_vggraph:
        for line in f_vggraph:
            vg_id, rel = line.split("\t")
            vg_id = int(vg_id)
            vg_graph_map[vg_id] = line
    vg_caption_map = {}
    with open(vg_caption_path) as f_vgcap:
        for line in f_vgcap:
            vg_id, _, rel = line.split("\t")
            vg_id = int(vg_id)
            vg_caption_map[vg_id] = line
    for caption_id in vg_caption_map:
        if caption_id in vg_graph_map:
            vgcap = vg_caption_map[caption_id]
            vggraph = vg_graph_map[caption_id]
            f_cap.write(vgcap)
            f_graph.write(vggraph)
    f_cap.close()
    f_graph.close()
def map_cococaption2vgcaption(datapath):
    vsgid2mscocoid = {}
    vg = json.load(open(datapath+"/vg_image_data.json"))
    for entry in vg:
        #print (enrtry['image_id'], enrtry['coco_id'])
        if entry['coco_id'] != None:
            print (entry['image_id'], entry['coco_id'])
            vsgid2mscocoid[entry['image_id']] = int(entry['coco_id'])
    print (vsgid2mscocoid)
    print ("vsg id =========================")
    for id in vsgid2mscocoid:
        print vsgid2mscocoid[id]
    print len(vsgid2mscocoid)

    cocoid2caption = {}
    with open(datapath+"mscoco_caption_map_clean.txt") as fcap:
        for line in fcap:
            #print line
            #line_parts = line.split("\t")
            cocoid, capt = line.split("\t")
            #print len(line_parts)
            #cocoid = line_parts[0]
            #capt = line_parts[1]

            #for i in range(2, len(line_parts)):
            #    capt = capt +" "+line_parts[i]

            cocoid2caption[int(cocoid)] = capt #int is bug?? definitely a big bug when read from file!!
    f_vgcap = open("vg_caption.txt","w")
    miss_count = 0
    for vg_id in vsgid2mscocoid:
        mapcocoid = vsgid2mscocoid[vg_id]
        try:
            vgcaption = cocoid2caption[mapcocoid]
            f_vgcap.write(str(vg_id)+"\t"+str(vgcaption))
        except:
            print ("Missing id = "+str(mapcocoid))
            miss_count += 1
    f_vgcap.close()
    print (miss_count)
    print ("done")
if __name__ == '__main__':
    #datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    #process_caption_data(datapath)
    data_filter()
    #generate_scene_graph_data(datapath)
    #map_cococaption2vgcaption(datapath)
    #f_cap = open("./data/mscoco_caption_map.txt", "a")
    #for id in cap_map:
    #    f_cap.write(str(id) + "\t" + str(cap_map[id]) + "\n")
