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
import edu.stanford.nlp.scenegraph.SceneGraph;
public class ComplexQueryImageSearch {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        //String sentence = "A brown fox chases a white rabbit.";
        String sentence = "A man and a woman sitting at a table with a cake";

        RuleBasedParser parser = new RuleBasedParser();
        SceneGraph sg = parser.parse(sentence);

        //printing the scene graph in a readable format
        System.out.println(sg.toReadableString()); 

        //printing the scene graph in JSON form
       // System.out.println(sg.toJSON()); 
    }
    
}
