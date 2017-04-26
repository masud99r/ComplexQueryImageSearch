/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package complexqueryimagesearch;

/**
 *
 * @author mr5ba
 */

import edu.stanford.nlp.scenegraph.RuleBasedParser;
import edu.stanford.nlp.scenegraph.KNNSceneGraphParser;
import edu.stanford.nlp.scenegraph.CRFDataExtractor;
import edu.stanford.nlp.scenegraph.SceneGraph;
import java.util.ArrayList;
import java.util.HashMap;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;


public class ComplexQueryImageSearch {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        //String sentence = "A brown fox chases a white rabbit.";
        RuleBasedParser parser = new RuleBasedParser();
        //String sentence = "A white rabbit.";
        String datapath = "K:/Masud/PythonProjects/ComplexQueryImageSearch/data_process/";
        BufferedReader br = null;
        String line= "";
        BufferedWriter bw = null;
        try {
            br = new BufferedReader(new FileReader(datapath+"vg_caption.txt"));
            FileWriter fw = new FileWriter("vg_caption_relation_attribute.txt");
            bw = new BufferedWriter(fw);
            while((line = br.readLine()) !=null ){
                System.out.println(line);
                String[] lineParts = line.split("\t");
                String vg_id = lineParts[0];
                String vg_caption = lineParts[1];
                //String sentence = "A man with a black twisted hat and a woman with blue dress sitting at a white rounded table with a red cake";
                SceneGraph sg = parser.parse(vg_caption);
                //printing the scene graph in a readable format
                //System.out.println(sg.toReadableString()); 
                //System.out.println(sg.nodeListSorted());
                //System.out.println(sg.toString());
                String sg_text = sg.toReadableString();
                String[] sgtext_parts = sg_text.split("\n");
                int collect_type = 0; //0 means relation
                int attribute_type = 0; //1 for active attr
                String attributeStr = "";
                String objectStr = "";
                ArrayList<String> relationshipList = new ArrayList<>();
                ArrayList<String> attributeList = new ArrayList<>();
                
                for(int i = 2;i<sgtext_parts.length;i++){
                    String clean_parts = sgtext_parts[i].trim().replaceAll(" +", " ");
                    //System.out.println(sgtext_parts[i].trim().replaceAll(" +", " "));
                    //System.out.println(clean_parts);
                    if(clean_parts.isEmpty()){
                        continue;
                    }
                    if (clean_parts.startsWith("Nodes")||clean_parts.startsWith("---")){
                        collect_type = 1;//1 for objects with attribute
                        continue;
                    }
                    if (clean_parts.startsWith("-")){
                        attribute_type = 1;//1 for objects with attribute
                        //System.out.println(objectStr+":"+clean_parts.replace("-", ""));
                        attributeList.add(objectStr+":"+clean_parts.replace("-", ""));
                    }
                    else if (collect_type == 1){
                        attribute_type = 0;
                        objectStr = clean_parts;
                        //objectStr
                    }
                    else{
                        attribute_type = 0;
                    }
                    if(collect_type==0){//relationship
                        //System.out.println("Rel:"+clean_parts);
                        relationshipList.add(clean_parts);
                    }
                    if(collect_type==1 && attribute_type == 0){//object
                        objectStr = clean_parts;
                    }

                }
                String relationships = "NONE";
                for(int i=0;i<relationshipList.size();i++){
                    relationships = relationships +","+relationshipList.get(i);
                }
                String attributes = "NONE";
                for(int i=0;i<attributeList.size();i++){
                    attributes = attributes +","+attributeList.get(i);
                }
                if (relationshipList.size()>= 2){
                    bw.write(vg_id+"\t"+vg_caption+"\t"+relationships+"\t"+attributes+"\t"+relationshipList.size()+"\t"+attributeList.size()+"\n");
                
                }
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            try {
                br.close();
                bw.close();
            } catch (IOException ex) {
                Logger.getLogger(ComplexQueryImageSearch.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        //printing the scene graph in JSON form
       // System.out.println(sg.toJSON()); 
    }
    
}
