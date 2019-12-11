
require(plyr)

c = read.csv2("cocktails.csv")
c[,1] = as.character(c[,1])

make.recipe = function(x){
    
    v = as.numeric(x)
    names(v) = names(x)
    v = v[!is.na(v)]
    print(v)
    

    str = paste0("\n(\"",names(v),"\", ",v,")",collapse=",")
    
    str = paste0("\"recipe\": [",str,"\n]")
    
    return(str)

}

r = ddply(c,.(X),make.recipe)
write.csv2(r,"recipes.csv")
