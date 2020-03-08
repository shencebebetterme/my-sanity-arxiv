using PyCall
@pyimport bs4

soup=bs4.BeautifulSoup(test_txt,"html.parser")
list=soup[:find](class="suggestions")[:find_all]("li");
for li in list
    word=li[:find](class="word")[:get_text]()
    def=li[:find](class="definition")[:get_text]()
    println("\033[1m $word \033[0m")
    println(def)
    print("\n")
    
end