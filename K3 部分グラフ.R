#%%
df_transform_raw <- bind_rows(lapply(sort(paste0(rep(c('Del','Ins','SNV'),4),'_mutant.frequency_',rep(c(0.01,0.4,0.5,0.6),3))),function(x){
    tmp_df <- df[,c('Type.of.chemical.modification',x)]
    tmp_df$Value <- tmp_df[,x]
    tmp_df$type <- strsplit(x,'_')[[1]][1]
    tmp_df$AF <- strsplit(x,'_')[[1]][3]
    return(tmp_df[,c('Type.of.chemical.modification','Value','AF','type')])}))
df_transform_raw[,'Group'] <- c('E1Ctrl'='Group1','91G'='Group1','92A'='Group1','93C'='Group1','94T'='Group1',
                      'E2Ctrl'='Group2','EtO'='Group2','S'='Group2',
                      'E2Ctrl'='Group3','LNA'='Group3','LNATC'='Group3')[df_transform_raw[,'Type.of.chemical.modification']]
#%%
library(ggplot2)
library(ggpubr)
library(patchwork)
library(dplyr)
#%%
df = read.csv('/Users/jasontingting/Desktop/df.txt',sep='\t')
colnames(df)
#%%
sort(paste0(rep(c('Del','Ins','SNV'),4),'_mutant.frequency_',rep(c(0.01,0.4,0.5,0.6),3)))
#%%
df_transform <- aggregate(list('Value'=df_transform_raw$Value),
                          by=list('Type.of.chemical.modification'=df_transform_raw$Type.of.chemical.modification,
                                  'AF'=df_transform_raw$AF,
                                  'type'=df_transform_raw$type,
                                  'Group'=df_transform_raw$Group),FUN = function(x) {c('mean' = mean(x), 'sd' = sd(x))})
df_transform$mean <- df_transform$Value[,'mean']
df_transform$sd <- df_transform$Value[,'sd']
df_transform$Value <- NULL
#%%
plot_AF_Group_box <- function(Group,AF){
    tmp_df <- df_transform[df_transform$Group==Group&df_transform$AF==AF,]
    tmp_df_raw <- df_transform_raw[df_transform_raw$Group==Group&df_transform$AF==AF,]
    my_comparisons <- combn(unique(tmp_df$Type.of.chemical.modification), 2)
    my_comparisons <- lapply(1:ncol(my_comparisons),function(x){return(my_comparisons[,x])})

    p1 <-
    ggplot(tmp_df_raw,aes(x=Type.of.chemical.modification,y=Value))+
    #geom_point(data=tmp_df_raw,aes(x=Type.of.chemical.modification,y=Value),color='black')+
    geom_bar(data=tmp_df,aes(x=Type.of.chemical.modification,y=mean,fill=Type.of.chemical.modification),color='black',lwd=0.5,width=0.8,stat='identity')+
    geom_errorbar(data=tmp_df,aes(x=Type.of.chemical.modification,y=mean,ymin = mean-sd, ymax = mean+sd), width = 0.2,color='black',lwd=0.5)+
    scale_fill_manual(values = c('#E64B35FF','#4DBBD5FF','#00A087FF','#3C5488FF',
                                 '#F39B7FFF','#8491B4FF',
                                 '#91D1C2FF','#DC0000FF','#7E6148FF','#B09C85FF'))+
    stat_compare_means(data=tmp_df_raw,mapping=aes(x=Type.of.chemical.modification,y=Value),comparisons = my_comparisons,label ="p.signif",size=6)+
    facet_wrap(~type,scale='free')+
    theme_classic()+
    theme(text = element_text(size=18))+
    ggtitle(paste0('AF=',AF,', ',Group))+
    ylab('Frequency')
    p1
}
#%%
stat_compare_means
#%%
for(i in c('0.01','0.4','0.5','0.6')){
    p <- plot_AF_Group_box('Group1',i)+
         plot_AF_Group_box('Group2',i)+
         plot_AF_Group_box('Group3',i)+plot_layout(nrow=3)
    pdf(paste0('R_Plot/','AF_',i,'.pdf'),width=15,height=16)
    print(p)
    dev.off()
}
#%%
options(repr.plot.width=15,repr.plot.height=16)
plot_AF_Group_box('Group1','0.6')+
plot_AF_Group_box('Group2','0.6')+
plot_AF_Group_box('Group3','0.6')+plot_layout(nrow=3)
