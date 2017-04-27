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

if __name__ == '__main__':
    #some samples
    fresh_text = remove_string_noise("	package com.test; public class C1 { private int[] nums; private void foo() { nums } } "
                          "------------------------------------------ In the above example, hover over 'nums' in foo()"
                          " and apply the quick fix \"Create 'for' loop\". It results in the following code: for (int i ="
                          " 0; i < nums.length; i++) { int i = nums[i]; } The local variable 'i' is duplicate "
                          "and has compilation error.")
    print fresh_text

    fresh_text = remove_string_noise(
        "org.eclipse.jdt.ui.tests/ui/org/eclipse/jdt/ui/tests/quickfix/AssistQuickFixTest.java,"
        "org.eclipse.jdt.ui/ui/org/eclipse/jdt/internal/ui/text/correction/IProposalRelevance.java,"
        "org.eclipse.jdt.ui/ui/org/eclipse/jdt/internal/ui/text/correction/proposals/GenerateForLoopAssistProposal.java")
    print fresh_text