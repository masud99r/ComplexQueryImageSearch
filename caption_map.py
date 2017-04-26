import random, json, string
def generate_caption_map(captionjsonpath):
    id2caps = {}
    mscoco = json.load(open(captionjsonpath))
    captionStrings = [entry['caption'].encode('ascii') for entry in mscoco['annotations']]
    mscoco_imageid = [entry['image_id'] for entry in mscoco['annotations']]

    for i in range(0, len(captionStrings)):
        imageid = mscoco_imageid[i]
        captiontext = captionStrings[i]
        captiontext = str(captiontext).replace("\t"," ").strip()#remove unwanted tab char (\t)
        '''
        # to get all the captions
        if imageid in id2caps:
            oldcaps = id2caps[imageid]
            newcaps = oldcaps +"\t"+captiontext
            id2caps[imageid] = newcaps
        '''
        if imageid in id2caps:
            oldcaps = id2caps[imageid]
            len_oldcaps = len(str(oldcaps).split(" "))
            len_captiontext = len(str(captiontext).split(" "))
            if(len_captiontext>len(oldcaps)):# if the new caption has more words than the old one
                id2caps[imageid] = captiontext
        else:
            id2caps[imageid] = captiontext

    return id2caps

if __name__ == '__main__':
    #mscoco_caption_train = "K:/Masud/2017Spring/Vision/language_generation_lab/annotations/captions_train2014.json"
    mscoco_caption_val = "K:/Masud/2017Spring/Vision/language_generation_lab/annotations/captions_val2014.json"
    cap_map = generate_caption_map(mscoco_caption_val)
    f_cap = open("./data/mscoco_caption_map.txt","a")
    for id in cap_map:
        f_cap.write(str(id)+"\t"+str(cap_map[id])+"\n")