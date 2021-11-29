library(ggplot2)
library(dplyr)

options(scipen=999)
uni.data <- readr::read_csv("actual_uniques.csv")

g <- ggplot(data = uni.data, aes(x=county, y=pct.uniques, fill=county)) +
  geom_bar(stat = "identity", color = "grey40", width=0.5) + 
  labs(y = "Percentage in Non-zeros (%)", x = "") +
  scale_fill_grey(start = 0.7, end = 0.9) +
  geom_text(aes(label=pct.uniques), position = position_dodge(0.9),
            vjust = 1.2, color = "grey20", size=2.5) +
  facet_grid(aggregation.level ~ query.type) +
  theme_bw()
g
ggsave(g, file="pct_actual.eps", device="eps")


#########
library(scales)
demo_continuous(c(1, 2, 3, 4), labels = label_math())

data.risks <- readr::read_csv("reid_risk_con.csv")
data.ppv <- data.risks[data.risks$risk.type == 'ppv',]
data.tpr <- data.risks[data.risks$risk.type == 'tpr',]

ppv <- ggplot(data = data.ppv, aes(x=log10(plb), y=risk.value, fill=county)) +
  scale_x_continuous(labels = label_math()) +
  geom_line(aes(linetype=county, color=county)) +
  geom_point(aes(shape=county, color=county)) +
  scale_shape_manual(values=c(19, 17)) +
  scale_colour_grey(start = 0.2, end = 0.7) +
  labs(y = "PPV", x = "") +
  scale_fill_grey(start = 0.7, end = 0.9) +
  facet_grid(aggregation.level ~ query.type) +
  theme_bw() +
  ylim(0, 0.6)
ppv
ggsave(ppv, file="ppv.eps", device="eps")

tpr <- ggplot(data = data.tpr, aes(x=log10(plb), y=risk.value, fill=county)) +
  scale_x_continuous(labels = label_math()) +
  geom_line(aes(linetype=county, color=county)) +
  geom_point(aes(shape=county, color=county)) +
  scale_shape_manual(values=c(19, 17)) +
  scale_colour_grey(start = 0.2, end = 0.7) +
  labs(y = "TPR", x = "") +
  scale_fill_grey(start = 0.7, end = 0.9) +
  facet_grid(aggregation.level ~ query.type) +
  theme_bw() +
  ylim(0, 0.6)
tpr
ggsave(tpr, file="tpr.eps", device="eps")
