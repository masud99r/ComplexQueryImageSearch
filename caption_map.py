import random, json, string
mscoco = json.load(open('K:/Masud/2017Spring/Vision/language_generation_lab/annotations/captions_val2014.json'))
captionStrings = ['[START] ' + entry['caption'].encode('ascii') for entry in mscoco['annotations']]
mscoco_imageid = [entry['image_id'] for entry in mscoco['annotations']]

print('Number of sentences', len(captionStrings))
print('First sentence in the list', captionStrings[0])
print('Second sentence in the list', captionStrings[1])
print('Third sentence in the list', captionStrings[2])

print('Total image size', len(mscoco_imageid))
print('First sentence in the list', mscoco_imageid[0])
print('Second sentence in the list', mscoco_imageid[1])
print('Third sentence in the list', mscoco_imageid[2])