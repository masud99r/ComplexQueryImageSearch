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
        print (str(entry['image_id']) + "_" + str(objectid))


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
                    print (str(image_id)+"_"+str(subject_objectid))
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


if __name__ == '__main__':
    #datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    datapath = "/if24/mr5ba/Masud/PythonProjects/ComplexQueryImageSearch/data/"
    generate_scene_graph_data(datapath)

    #f_cap = open("./data/mscoco_caption_map.txt", "a")
    #for id in cap_map:
    #    f_cap.write(str(id) + "\t" + str(cap_map[id]) + "\n")