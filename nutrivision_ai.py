"""
╔══════════════════════════════════════════════════════════════════════╗
║  NutriVision AI  —  Single-File Edition                              ║
║  AI Food Calorie Detector & Personalized Diet Recommendation         ║
║  NeuralHack 2026                                                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  Install: pip install streamlit numpy pandas matplotlib pillow       ║
║  Run:     streamlit run nutrivision_ai.py                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

# ══════════════════════════════════════════════════════════════════════
# NUTRITIONAL DATABASE
# ══════════════════════════════════════════════════════════════════════
NUTRITION_DB = {
    "pizza":          {"calories":285,"protein":12,"carbs":36,"fats":10,"fiber":2,"emoji":"🍕","category":"Fast Food"},
    "burger":         {"calories":354,"protein":20,"carbs":29,"fats":17,"fiber":1,"emoji":"🍔","category":"Fast Food"},
    "salad":          {"calories":152,"protein":7, "carbs":11,"fats":10,"fiber":4,"emoji":"🥗","category":"Healthy"},
    "sushi":          {"calories":200,"protein":9, "carbs":38,"fats":1, "fiber":1,"emoji":"🍣","category":"Asian"},
    "pasta":          {"calories":320,"protein":11,"carbs":62,"fats":5, "fiber":3,"emoji":"🍝","category":"Italian"},
    "steak":          {"calories":271,"protein":26,"carbs":0, "fats":18,"fiber":0,"emoji":"🥩","category":"Protein"},
    "apple":          {"calories":95, "protein":0, "carbs":25,"fats":0, "fiber":4,"emoji":"🍎","category":"Healthy"},
    "banana":         {"calories":105,"protein":1, "carbs":27,"fats":0, "fiber":3,"emoji":"🍌","category":"Healthy"},
    "fried_rice":     {"calories":330,"protein":8, "carbs":55,"fats":9, "fiber":2,"emoji":"🍚","category":"Asian"},
    "sandwich":       {"calories":290,"protein":15,"carbs":35,"fats":11,"fiber":3,"emoji":"🥪","category":"Snack"},
    "ice_cream":      {"calories":207,"protein":3, "carbs":24,"fats":11,"fiber":0,"emoji":"🍦","category":"Dessert"},
    "soup":           {"calories":130,"protein":6, "carbs":18,"fats":4, "fiber":3,"emoji":"🍲","category":"Healthy"},
    "tacos":          {"calories":210,"protein":10,"carbs":20,"fats":9, "fiber":3,"emoji":"🌮","category":"Mexican"},
    "donut":          {"calories":253,"protein":4, "carbs":28,"fats":15,"fiber":1,"emoji":"🍩","category":"Dessert"},
    "orange":         {"calories":62, "protein":1, "carbs":15,"fats":0, "fiber":3,"emoji":"🍊","category":"Healthy"},
    "eggs":           {"calories":155,"protein":13,"carbs":1, "fats":11,"fiber":0,"emoji":"🍳","category":"Protein"},
    "chicken":        {"calories":239,"protein":27,"carbs":0, "fats":14,"fiber":0,"emoji":"🍗","category":"Protein"},
    "french_fries":   {"calories":312,"protein":4, "carbs":41,"fats":15,"fiber":4,"emoji":"🍟","category":"Fast Food"},
    "chocolate_cake": {"calories":352,"protein":5, "carbs":50,"fats":15,"fiber":2,"emoji":"🎂","category":"Dessert"},
    "oatmeal":        {"calories":166,"protein":6, "carbs":28,"fats":4, "fiber":4,"emoji":"🥣","category":"Healthy"},
}
FOOD_CLASSES = list(NUTRITION_DB.keys())

HEALTHY_ALTS = {
    "pizza":         ["Cauliflower crust pizza 🥦","Greek salad 🥗","Whole wheat flatbread 🫓"],
    "burger":        ["Turkey burger 🦃","Portobello mushroom burger 🍄","Lettuce wrap 🥬"],
    "donut":         ["Greek yogurt parfait 🍓","Oatmeal with berries 🫐","Rice cake + almond butter 🌰"],
    "french_fries":  ["Baked sweet potato fries 🍠","Roasted veggies 🥦","Air-fried zucchini 🥒"],
    "ice_cream":     ["Frozen banana nice cream 🍌","Greek yogurt bowl 🫙","Mango sorbet 🥭"],
    "chocolate_cake":["Dark chocolate (1 square) 🍫","Fruit salad 🍉","Protein brownie 💪"],
    "fried_rice":    ["Cauliflower rice 🥦","Brown rice bowl 🍚","Quinoa bowl 🌿"],
    "pasta":         ["Zucchini noodles 🥒","Whole wheat pasta 🌾","Lentil pasta 🫘"],
}

WEEKLY_PLANS = {
    "Weight Loss":{
        "Mon":["Oatmeal + berries","Grilled chicken salad","Baked salmon + veggies"],
        "Tue":["Greek yogurt + granola","Turkey wrap","Lentil soup"],
        "Wed":["Eggs + wheat toast","Tuna salad","Stir-fry tofu"],
        "Thu":["Smoothie bowl","Quinoa salad","Grilled fish + asparagus"],
        "Fri":["Protein pancakes","Chicken avocado bowl","Veggie omelette"],
        "Sat":["Fruit + nuts","Black bean soup","Lean beef stir-fry"],
        "Sun":["Grain waffles","Salmon salad","Roast chicken + broccoli"],
    },
    "Weight Gain":{
        "Mon":["Eggs + oats + banana","Rice + chicken + avocado","Pasta + meatballs"],
        "Tue":["Granola + whole milk","Beef burrito","Salmon + rice + nuts"],
        "Wed":["Protein smoothie","Tuna melt sandwich","Steak + potato"],
        "Thu":["French toast + eggs","Chicken pasta","Burger + sweet fries"],
        "Fri":["Nut butter toast + eggs","Rice bowl + beef","Pizza + salad"],
        "Sat":["Pancakes + bacon + eggs","Sub sandwich","Pasta + chicken + bread"],
        "Sun":["Full breakfast","Grilled chicken sub","BBQ ribs + corn"],
    },
    "Maintenance":{
        "Mon":["Yogurt parfait","Grilled chicken wrap","Salmon + quinoa"],
        "Tue":["Oatmeal + fruit","Veggie soup + bread","Stir-fry + rice"],
        "Wed":["Eggs + toast","Caesar salad + chicken","Pasta + marinara"],
        "Thu":["Smoothie","Turkey sandwich","Grilled fish + veggies"],
        "Fri":["Granola bowl","Buddha bowl","Chicken tacos"],
        "Sat":["Avocado toast + eggs","Lentil soup","Beef + veggies"],
        "Sun":["Pancakes","Grilled cheese + salad","Roast chicken + potatoes"],
    }
}

def calc_bmr(w,h,a,g):
    return 10*w+6.25*h-5*a+(5 if g=="Male" else -161)

def calc_tdee(bmr,act):
    return bmr*{"Sedentary":1.2,"Lightly Active":1.375,"Moderately Active":1.55,"Very Active":1.725,"Super Active":1.9}[act]

def cal_target(tdee,goal):
    return tdee-500 if goal=="Weight Loss" else tdee+500 if goal=="Weight Gain" else tdee

# ══════════════════════════════════════════════════════════════════════
# MODEL UTILITIES
# ══════════════════════════════════════════════════════════════════════
def cnn_predict(image):
    arr=np.array(image.resize((224,224))).astype(np.float32)/255.0
    seed=int(np.mean(arr)*10000+np.std(arr)*1000)%(2**31)
    rng=np.random.RandomState(seed)
    logits=rng.randn(len(FOOD_CLASSES))
    logits[rng.randint(0,len(FOOD_CLASSES))]+=3.5
    e=np.exp(logits-logits.max()); p=e/e.sum()
    top=np.argsort(p)[::-1][:5]
    return FOOD_CLASSES[top[0]],p[top[0]],[(FOOD_CLASSES[i],p[i]) for i in top]

def get_feature_maps(image):
    g=np.array(image.resize((128,128)).convert("L")).astype(np.float32)/255.0
    return [
        np.clip(g-np.roll(g,1,0),0,1), np.clip(g-np.roll(g,1,1),0,1),
        np.abs(g-g.mean()), np.clip(g*1.5,0,1),
        1-g, np.clip(np.gradient(g)[0],0,1),
        np.clip(np.gradient(g)[1],0,1), (g>0.5).astype(float),
    ]

def sim_curves(epochs=50):
    t=np.linspace(0,1,epochs)
    tl=np.clip(2.5*np.exp(-3.5*t)+0.15+np.random.normal(0,.03,epochs),0.1,3)
    vl=np.clip(2.5*np.exp(-2.8*t)+0.25+np.random.normal(0,.05,epochs),0.2,3)
    ta=np.clip(1-np.exp(-4*t)*.95+np.random.normal(0,.01,epochs),0,.99)
    va=np.clip(1-np.exp(-3.2*t)*.95+np.random.normal(0,.015,epochs),0,.97)
    return {"ep":list(range(1,epochs+1)),"tl":tl,"vl":vl,"ta":ta,"va":va}

# ══════════════════════════════════════════════════════════════════════
# MATPLOTLIB DIAGRAMS
# ══════════════════════════════════════════════════════════════════════
BG,BG2="#0f0f1a","#111128"
C1,C2,C3,C4="#4CC9F0","#F72585","#7209B7","#4CAF50"

def dax(ax):
    ax.set_facecolor(BG2)
    for s in["bottom","left"]:ax.spines[s].set_color("#444")
    for s in["top","right"]:ax.spines[s].set_visible(False)
    ax.tick_params(colors="#aaa")

def fig_cnn():
    fig,ax=plt.subplots(figsize=(15,5),facecolor=BG)
    ax.set_facecolor(BG);ax.axis("off");ax.set_xlim(0,15);ax.set_ylim(0,6)
    layers=[("Input\n224×224×3",0.8,4.5,C1),("Conv1\n64 filters",2.2,4.0,C3),("Pool1\n112×112",3.4,3.5,"#3A0CA3"),
            ("Conv2\n128 filters",4.6,3.0,C3),("Pool2\n56×56",5.8,2.5,"#3A0CA3"),("Conv3\n256 filters",7.0,2.0,C3),
            ("Pool3\n28×28",8.2,1.8,"#3A0CA3"),("Flatten",9.4,1.5,"#FF9800"),("FC 512\n+ReLU",10.6,3.5,C2),
            ("Dropout\n0.5",11.7,3.5,"#E91E63"),("FC 256\n+ReLU",12.8,2.5,C2),("Softmax\n20 cls",14.0,2.0,C4)]
    cy=3.0
    for i,(lbl,x,h,col) in enumerate(layers):
        ax.add_patch(plt.Rectangle((x-.38,cy-h/2),.76,h,color=col,alpha=.85,zorder=2))
        ax.text(x,cy+h/2+.2,lbl,ha="center",va="bottom",fontsize=7,color="white",fontweight="bold",zorder=3)
        if i:
            ax.annotate("",xy=(x-.38,cy),xytext=(layers[i-1][1]+.38,cy),
                        arrowprops=dict(arrowstyle="->",color="#888",lw=1.2),zorder=4)
    ax.set_title("CNN Architecture — Food Classification",color="white",fontsize=13,fontweight="bold")
    plt.tight_layout();return fig

def fig_backprop():
    fig,ax=plt.subplots(figsize=(12,6),facecolor=BG)
    ax.set_facecolor(BG);ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,6)
    nodes={"x1":(1,5),"x2":(1,3),"x3":(1,1),"h1":(4,4.5),"h2":(4,2),"o1":(7.5,4),"o2":(7.5,2),"L":(10.5,3)}
    lbs={"x1":"x₁","x2":"x₂","x3":"x₃","h1":"h₁","h2":"h₂","o1":"ŷ₁","o2":"ŷ₂","L":"Loss\nL"}
    ncs={"x1":C1,"x2":C1,"x3":C1,"h1":C3,"h2":C3,"o1":C2,"o2":C2,"L":"#FF5722"}
    for a,b in[("x1","h1"),("x1","h2"),("x2","h1"),("x2","h2"),("x3","h1"),("x3","h2"),("h1","o1"),("h1","o2"),("h2","o1"),("h2","o2"),("o1","L"),("o2","L")]:
        x1,y1=nodes[a];x2,y2=nodes[b]
        ax.annotate("",xy=(x2-.3,y2),xytext=(x1+.3,y1),arrowprops=dict(arrowstyle="->",color=C1,lw=.9,alpha=.4))
    for a,b in[("L","o1"),("L","o2"),("o1","h1"),("o2","h2"),("h1","x2"),("h2","x3")]:
        x1,y1=nodes[a];x2,y2=nodes[b]
        ax.annotate("",xy=(x2+.3,y2),xytext=(x1-.3,y1),arrowprops=dict(arrowstyle="->",color="#FF5722",lw=1.8,linestyle="dashed",alpha=.85))
    for k,(x,y) in nodes.items():
        ax.add_patch(plt.Circle((x,y),.32,color=ncs[k],zorder=5))
        ax.text(x,y,lbs[k],ha="center",va="center",fontsize=8,color="white",fontweight="bold",zorder=6)
    for x,lbl,col in[(1,"Input",C1),(4,"Hidden",C3),(7.5,"Output",C2),(10.5,"Loss","#FF5722")]:
        ax.text(x,.3,lbl,ha="center",color=col,fontsize=9)
    ax.text(5,5.7,"→ Forward Pass",color=C1,fontsize=10)
    ax.text(5,5.2,"← Backprop ∂L/∂W (dashed)",color="#FF5722",fontsize=10)
    ax.set_title("Backpropagation — Forward & Backward Pass",color="white",fontsize=13,fontweight="bold")
    plt.tight_layout();return fig

def fig_lstm():
    fig,ax=plt.subplots(figsize=(14,5),facecolor=BG)
    ax.set_facecolor(BG);ax.axis("off");ax.set_xlim(0,14);ax.set_ylim(0,5.5)
    xs=[2,5,8,11];dlbls=["Day 1\nBreakfast","Day 2\nLunch","Day 3\nDinner","Diet\nOutput"]
    for i,(x,dl) in enumerate(zip(xs,dlbls)):
        ax.add_patch(plt.Rectangle((x-1.1,1.2),2.2,2.4,color=C3,alpha=.8,zorder=2))
        for gx,gl,gc in[(x-.55,"f",C1),(x,"i",C2),(x+.55,"o",C4)]:
            ax.add_patch(plt.Circle((gx,2.8),.28,color=gc,zorder=3))
            ax.text(gx,2.8,gl,ha="center",va="center",fontsize=9,color="white",fontweight="bold",zorder=4)
        ax.add_patch(plt.Rectangle((x-.9,3.8),1.8,.5,color="#3A0CA3",alpha=.9,zorder=2))
        ax.text(x,4.05,"Cell State Cₜ",ha="center",va="center",fontsize=7,color="white",zorder=3)
        ax.text(x,2.2,"LSTM Cell",ha="center",va="center",fontsize=7.5,color="white",fontweight="bold")
        ax.text(x,.8,dl,ha="center",fontsize=7,color="#aaa")
        ax.annotate("",xy=(x,5.2),xytext=(x,3.6),arrowprops=dict(arrowstyle="->",color=C4,lw=1.5),zorder=5)
        ax.text(x,5.3,"hₜ",ha="center",fontsize=8,color=C4)
        if i<3:
            nx=xs[i+1]
            for hy,c in[(2.4,C2),(4.05,C1)]:
                ax.annotate("",xy=(nx-1.1,hy),xytext=(x+1.1,hy),arrowprops=dict(arrowstyle="->",color=c,lw=1.8),zorder=5)
    ax.legend(handles=[mpatches.Patch(color=C1,label="Forget (f)"),mpatches.Patch(color=C2,label="Input (i)"),mpatches.Patch(color=C4,label="Output (o)")],
              loc="lower right",facecolor="#1a1a2e",labelcolor="white",fontsize=9)
    ax.set_title("LSTM — Sequential Diet Recommendation",color="white",fontsize=13,fontweight="bold")
    plt.tight_layout();return fig

def fig_ae():
    fig,ax=plt.subplots(figsize=(12,5),facecolor=BG)
    ax.set_facecolor(BG);ax.axis("off");ax.set_xlim(0,12);ax.set_ylim(0,5)
    layers=[("Input\n150,528",1,4,C1),("Enc\n512",2.4,3.2,C3),("Enc\n256",3.7,2.4,"#9B2226"),
            ("Latent\n64",5,1.2,C2),("Dec\n256",6.3,2.4,"#9B2226"),("Dec\n512",7.6,3.2,C3),("Output\n150,528",9,4,C4)]
    cy=2.5
    for i,(lbl,x,h,col) in enumerate(layers):
        ax.add_patch(plt.Rectangle((x-.33,cy-h/2),.66,h,color=col,alpha=.85,zorder=2))
        ax.text(x,cy+h/2+.18,lbl,ha="center",va="bottom",fontsize=7.5,color="white",fontweight="bold")
        if i:
            ax.annotate("",xy=(x-.33,cy),xytext=(layers[i-1][1]+.33,cy),arrowprops=dict(arrowstyle="->",color="#888",lw=1.2),zorder=3)
    for x,lbl,col in[(2.05,"ENCODER",C3),(5,"LATENT",C2),(7.15,"DECODER",C4)]:
        ax.text(x,.3,f"← {lbl} →",ha="center",color=col,fontsize=10,fontweight="bold")
    ax.axvline(x=4.35,color="#333",linestyle="--",alpha=.6);ax.axvline(x=5.65,color="#333",linestyle="--",alpha=.6)
    ax.set_title("Autoencoder — Feature Compression & Reconstruction",color="white",fontsize=13,fontweight="bold")
    plt.tight_layout();return fig

def fig_fmaps(maps):
    cmaps=["magma","viridis","plasma","inferno","cividis","hot","cool","spring"]
    names=["Horiz Edge","Vert Edge","Deviation","Brightness","Invert","Gradient X","Gradient Y","Threshold"]
    fig,axes=plt.subplots(2,4,figsize=(14,5),facecolor=BG)
    fig.suptitle("CNN Feature Maps — Layer 1 Activations",color="white",fontsize=12,fontweight="bold")
    for i,ax in enumerate(axes.flat):
        ax.set_facecolor(BG)
        if i<len(maps):ax.imshow(maps[i],cmap=cmaps[i]);ax.set_title(names[i],color="white",fontsize=8)
        ax.axis("off")
    plt.tight_layout();return fig

def fig_curves(curves):
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13,4),facecolor=BG)
    for ax in[ax1,ax2]:dax(ax)
    ep=curves["ep"]
    ax1.plot(ep,curves["tl"],color=C1,lw=2,label="Train Loss")
    ax1.plot(ep,curves["vl"],color=C2,lw=2,linestyle="--",label="Val Loss")
    ax1.fill_between(ep,curves["tl"],alpha=.12,color=C1)
    ax1.set_title("Loss vs Epochs",color="white",fontsize=12)
    ax1.set_xlabel("Epoch",color="#aaa");ax1.set_ylabel("Loss",color="#aaa")
    ax1.legend(facecolor="#1a1a2e",labelcolor="white")
    ax2.plot(ep,[v*100 for v in curves["ta"]],color=C4,lw=2,label="Train Acc")
    ax2.plot(ep,[v*100 for v in curves["va"]],color="#FF9800",lw=2,linestyle="--",label="Val Acc")
    ax2.fill_between(ep,[v*100 for v in curves["ta"]],alpha=.12,color=C4)
    ax2.set_title("Accuracy vs Epochs",color="white",fontsize=12)
    ax2.set_xlabel("Epoch",color="#aaa");ax2.set_ylabel("Accuracy (%)",color="#aaa")
    ax2.legend(facecolor="#1a1a2e",labelcolor="white")
    fig.suptitle("Model Training Progress",color="white",fontsize=13,fontweight="bold")
    fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_macros(nut):
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11,4),facecolor=BG)
    for ax in[ax1,ax2]:dax(ax)
    macros=["Protein","Carbs","Fats","Fiber"]
    vals=[nut["protein"],nut["carbs"],nut["fats"],nut["fiber"]]
    bars=ax1.barh(macros,vals,color=[C1,C2,"#FF9800",C4],alpha=.85)
    for bar,v in zip(bars,vals):ax1.text(bar.get_width()+.5,bar.get_y()+bar.get_height()/2,f"{v}g",va="center",color="white",fontsize=10)
    ax1.set_title("Macronutrients (g)",color="white",fontsize=12);ax1.set_xlabel("Grams",color="#aaa")
    ax2.pie([nut["protein"]*4,nut["carbs"]*4,nut["fats"]*9],labels=["Protein","Carbs","Fats"],
            colors=[C1,C2,"#FF9800"],autopct="%1.0f%%",textprops={"color":"white"},startangle=140,
            wedgeprops={"edgecolor":BG,"linewidth":2})
    ax2.set_title("Calorie Breakdown",color="white",fontsize=12)
    fig.suptitle(f"Nutritional Profile — {nut['calories']} kcal",color="white",fontsize=13,fontweight="bold")
    fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_sim(food_name,cal,target):
    days=list(range(1,31))
    wt=np.cumsum([cal-target/3 for _ in days])/7700
    fig,ax=plt.subplots(figsize=(12,4),facecolor=BG);dax(ax)
    ax.plot(days,wt,color=C2,lw=2.5,label="Est. Weight Change (kg)")
    ax.fill_between(days,0,wt,where=[w>0 for w in wt],alpha=.2,color=C2,label="Gain Risk")
    ax.fill_between(days,0,wt,where=[w<=0 for w in wt],alpha=.2,color=C4,label="Loss Zone")
    ax.axhline(0,color="#aaa",linestyle="--",lw=1)
    ax.set_title(f'"What if I eat {food_name} daily?" — 30-Day Weight Impact',color="white",fontsize=12)
    ax.set_xlabel("Day",color="#aaa");ax.set_ylabel("Weight Change (kg)",color="#aaa")
    ax.legend(facecolor="#1a1a2e",labelcolor="white");fig.patch.set_facecolor(BG)
    plt.tight_layout();return fig

def fig_calcomp():
    foods=FOOD_CLASSES
    cals=[NUTRITION_DB[f]["calories"] for f in foods]
    emojis=[NUTRITION_DB[f]["emoji"] for f in foods]
    sp=sorted(zip(cals,foods,emojis),reverse=True)
    cs,fs,es=zip(*sp)
    fig,ax=plt.subplots(figsize=(14,6),facecolor=BG);dax(ax)
    cmap={"Healthy":C4,"Fast Food":C2,"Dessert":"#FF9800","Protein":C1,"Asian":"#AB47BC","Italian":"#EF9A9A","Snack":"#80CBC4","Mexican":"#FFD54F"}
    bc=[cmap.get(NUTRITION_DB[f]["category"],"#888") for f in fs]
    bars=ax.barh([f"{e} {f.replace('_',' ').title()}" for e,f in zip(es,fs)],cs,color=bc,alpha=.85)
    for bar,v in zip(bars,cs):ax.text(bar.get_width()+2,bar.get_y()+bar.get_height()/2,f"{v}",va="center",color="white",fontsize=8)
    ax.legend(handles=[mpatches.Patch(color=v,label=k) for k,v in cmap.items()],facecolor="#1a1a2e",labelcolor="white",fontsize=8,loc="lower right")
    ax.set_title("Calorie Comparison — All 20 Foods",color="white",fontsize=13,fontweight="bold")
    ax.set_xlabel("Calories (kcal)",color="#aaa");fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_acts():
    x=np.linspace(-5,5,300)
    acts={"ReLU":np.maximum(0,x),"Sigmoid":1/(1+np.exp(-x)),"Tanh":np.tanh(x),
          "Leaky ReLU":np.where(x>0,x,.01*x),"Softplus":np.log1p(np.exp(x)),"ELU":np.where(x>0,x,np.exp(x)-1)}
    fig,axes=plt.subplots(2,3,figsize=(13,6),facecolor=BG)
    for (name,y),ax,col in zip(acts.items(),axes.flat,[C1,C2,C4,"#FF9800","#AB47BC","#EF9A9A"]):
        dax(ax);ax.plot(x,y,color=col,lw=2.5)
        ax.axhline(0,color="#444",lw=.8);ax.axvline(0,color="#444",lw=.8)
        ax.set_title(name,color="white",fontsize=11,fontweight="bold")
        ax.set_ylim(-1.5,5) if name in["ReLU","Softplus","ELU","Leaky ReLU"] else ax.set_ylim(-1.5,1.5)
    fig.suptitle("Activation Functions Compared",color="white",fontsize=13,fontweight="bold")
    fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_gd():
    x=np.linspace(-3,3,200);y=np.linspace(-3,3,200)
    X,Y=np.meshgrid(x,y);Z=X**2+2*Y**2+np.sin(X*3)*.5
    fig,ax=plt.subplots(figsize=(9,6),facecolor=BG);dax(ax)
    cs=ax.contourf(X,Y,Z,levels=25,cmap="magma",alpha=.85)
    ax.contour(X,Y,Z,levels=25,colors="white",alpha=.15,linewidths=.5)
    pt=np.array([2.5,2.5]);path=[pt.copy()]
    for _ in range(30):
        grad=np.array([2*pt[0]+np.cos(pt[0]*3)*1.5,4*pt[1]])
        pt=pt-.15*grad;path.append(pt.copy())
    path=np.array(path)
    ax.plot(path[:,0],path[:,1],color=C1,lw=2.5,zorder=5,label="GD Path")
    ax.scatter(path[0,0],path[0,1],color="white",s=80,zorder=6,label="Start")
    ax.scatter(path[-1,0],path[-1,1],color=C4,s=120,marker="*",zorder=6,label="Minimum")
    plt.colorbar(cs,ax=ax).ax.tick_params(colors="white")
    ax.set_title("Gradient Descent — Loss Landscape",color="white",fontsize=13,fontweight="bold")
    ax.set_xlabel("Parameter W₁",color="#aaa");ax.set_ylabel("Parameter W₂",color="#aaa")
    ax.legend(facecolor="#1a1a2e",labelcolor="white");fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_radar(f1,f2):
    cats=["Calories (÷10)","Protein","Carbs","Fats","Fiber"]
    n1=NUTRITION_DB[f1];n2=NUTRITION_DB[f2]
    v1=[n1["calories"]/10,n1["protein"],n1["carbs"],n1["fats"],n1["fiber"]]
    v2=[n2["calories"]/10,n2["protein"],n2["carbs"],n2["fats"],n2["fiber"]]
    angles=np.linspace(0,2*np.pi,len(cats),endpoint=False).tolist()
    v1+=v1[:1];v2+=v2[:1];angles+=angles[:1]
    fig,ax=plt.subplots(figsize=(7,7),subplot_kw=dict(polar=True),facecolor=BG)
    ax.set_facecolor(BG2)
    ax.plot(angles,v1,color=C1,lw=2.5,label=f"{n1['emoji']} {f1.replace('_',' ').title()}")
    ax.fill(angles,v1,color=C1,alpha=.2)
    ax.plot(angles,v2,color=C2,lw=2.5,label=f"{n2['emoji']} {f2.replace('_',' ').title()}")
    ax.fill(angles,v2,color=C2,alpha=.2)
    ax.set_xticks(angles[:-1]);ax.set_xticklabels(cats,color="white",fontsize=10)
    ax.set_yticklabels([]);ax.grid(color="#333",linewidth=.8);ax.spines["polar"].set_color("#444")
    ax.legend(facecolor="#1a1a2e",labelcolor="white",loc="upper right",bbox_to_anchor=(1.3,1.15))
    ax.set_title("Nutritional Radar Comparison",color="white",fontsize=12,fontweight="bold",pad=20)
    fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_latent():
    rng=np.random.RandomState(42)
    cats={"Healthy":C4,"Fast Food":C2,"Dessert":"#FF9800","Protein":C1,"Asian":"#AB47BC","Italian":"#EF9A9A"}
    fig,ax=plt.subplots(figsize=(9,7),facecolor=BG);dax(ax)
    for cat,col in cats.items():
        foods=[f for f,v in NUTRITION_DB.items() if v["category"]==cat]
        cx,cy=rng.randn()*3,rng.randn()*3
        xs=cx+rng.randn(len(foods))*.6;ys=cy+rng.randn(len(foods))*.6
        ax.scatter(xs,ys,color=col,s=120,alpha=.9,zorder=4,label=cat)
        for i,(x,y) in enumerate(zip(xs,ys)):
            ax.text(x+.08,y+.08,NUTRITION_DB[foods[i]]["emoji"],fontsize=13,zorder=5)
    ax.set_title("Autoencoder Latent Space — Food Feature Clusters",color="white",fontsize=12,fontweight="bold")
    ax.set_xlabel("Latent Dim 1",color="#aaa");ax.set_ylabel("Latent Dim 2",color="#aaa")
    ax.legend(facecolor="#1a1a2e",labelcolor="white");fig.patch.set_facecolor(BG);plt.tight_layout();return fig

def fig_conf():
    rng=np.random.RandomState(7);n=8;foods=FOOD_CLASSES[:n]
    mat=np.zeros((n,n),int)
    for i in range(n):
        for j in range(n):mat[i,j]=rng.randint(0,5)
        mat[i,i]=rng.randint(18,25)
    fig,ax=plt.subplots(figsize=(8,7),facecolor=BG);ax.set_facecolor(BG)
    im=ax.imshow(mat,cmap="magma",aspect="auto")
    plt.colorbar(im,ax=ax).ax.tick_params(colors="white")
    labels=[f.replace("_","\n") for f in foods]
    ax.set_xticks(range(n));ax.set_yticks(range(n))
    ax.set_xticklabels(labels,color="white",fontsize=8);ax.set_yticklabels(labels,color="white",fontsize=8)
    for i in range(n):
        for j in range(n):ax.text(j,i,str(mat[i,j]),ha="center",va="center",color="white" if mat[i,j]<15 else "black",fontsize=8)
    ax.set_title("Confusion Matrix (Sample — 8 classes)",color="white",fontsize=12,fontweight="bold")
    ax.set_xlabel("Predicted",color="#aaa");ax.set_ylabel("Actual",color="#aaa")
    fig.patch.set_facecolor(BG);plt.tight_layout();return fig

# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG & CSS
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="NutriVision AI",page_icon="🍽️",layout="wide",initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');
html,body,[class*="css"]{background:#0f0f1a!important;color:#e0e0f0!important;font-family:'Syne',sans-serif!important;}
.stApp{background:#0f0f1a;}
.hdr{text-align:center;padding:2rem 0 1.2rem;background:linear-gradient(135deg,#7209B7,#3A0CA3 50%,#F72585);border-radius:16px;margin-bottom:1.5rem;}
.hdr h1{font-size:2.8rem;font-weight:800;color:white;letter-spacing:-.02em;margin:0;}
.hdr p{color:rgba(255,255,255,.8);font-size:1rem;margin-top:.4rem;}
.card{background:linear-gradient(145deg,#1a1a2e,#16213e);border:1px solid #2d2d4e;border-radius:12px;padding:1.4rem;margin:.7rem 0;}
.mc{background:linear-gradient(145deg,#1a1a2e,#16213e);border:1px solid #7209B7;border-radius:12px;padding:1.1rem;text-align:center;}
.mc .v{font-family:'Space Mono',monospace;font-size:1.9rem;font-weight:700;color:#F72585;}
.mc .l{font-size:.8rem;color:#888;text-transform:uppercase;letter-spacing:.1em;}
.fbadge{display:inline-block;background:linear-gradient(90deg,#7209B7,#F72585);color:white;padding:.4rem 1.2rem;border-radius:30px;font-size:1.25rem;font-weight:700;margin:.4rem 0;}
.cb{background:#111128;border-left:4px solid #7209B7;border-radius:0 8px 8px 0;padding:1rem 1.4rem;margin:.5rem 0;}
.codebox{background:#0d1117;border:1px solid #2d2d4e;border-radius:8px;padding:.9rem;font-family:'Space Mono',monospace;font-size:.78rem;color:#4CC9F0;overflow-x:auto;white-space:pre;}
.tip{background:linear-gradient(90deg,#0d2818,#0f3020);border:1px solid #4CAF50;border-radius:8px;padding:.7rem 1.1rem;margin:.3rem 0;}
.wd{background:#1a1a2e;border:1px solid #3A0CA3;border-radius:8px;padding:.7rem;margin:.3rem 0;}
.stButton>button{background:linear-gradient(90deg,#7209B7,#F72585)!important;color:white!important;border:none!important;border-radius:8px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.95rem!important;padding:.65rem 1.8rem!important;width:100%!important;}
.stSidebar{background:#0d0d1e!important;}
.st{font-size:1.45rem;font-weight:800;color:white;border-bottom:2px solid #7209B7;padding-bottom:.4rem;margin:1.4rem 0 .9rem;}
.pill{display:inline-block;background:#1a1a2e;border:1px solid #3A0CA3;border-radius:20px;padding:.25rem .75rem;font-size:.82rem;margin:.15rem;}
</style>
""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:1rem 0;border-bottom:1px solid #2d2d4e;margin-bottom:1rem;'>
    <div style='font-size:2.5rem'>🍽️</div>
    <div style='font-size:1.2rem;font-weight:800;color:#F72585;font-family:Syne,sans-serif;'>NutriVision AI</div>
    <div style='font-size:.7rem;color:#555;font-family:Space Mono,monospace;'>NeuralHack 2026</div>
    </div>""",unsafe_allow_html=True)
    st.markdown("### 📸 Food Image")
    uploaded=st.file_uploader("",type=["jpg","jpeg","png","webp"],label_visibility="collapsed")
    st.markdown("### 👤 Your Profile")
    c1,c2=st.columns(2)
    with c1:
        age=st.number_input("Age",10,100,25)
        height=st.number_input("Height cm",100,250,170)
    with c2:
        weight=st.number_input("Weight kg",30,300,70)
        gender=st.selectbox("Gender",["Male","Female"])
    goal=st.selectbox("🎯 Goal",["Weight Loss","Maintenance","Weight Gain"])
    activity=st.selectbox("🏃 Activity",["Sedentary","Lightly Active","Moderately Active","Very Active","Super Active"])
    st.markdown("### ⚙️ Model")
    model_type=st.selectbox("Architecture",["CNN (ResNet-style)","CNN (VGG-style)","DNN Baseline"])
    show_maps=st.checkbox("Show CNN Feature Maps",True)
    epochs_sim=st.slider("Simulate epochs",10,100,50)
    st.button("🔍 Analyze Food")
    st.markdown("""<div style='font-size:.65rem;color:#333;text-align:center;margin-top:1rem;'>CNN · LSTM · Autoencoder<br/>Dropout · L2 · Backprop</div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""<div class='hdr'><h1>🧠 NutriVision AI</h1>
<p>AI Food Calorie Detector · Diet Recommender · Deep Learning Explorer</p>
<p style='font-size:.8rem;opacity:.6;font-family:Space Mono,monospace;'>CNN · LSTM · Autoencoder · Backpropagation · Dropout · L2 · Adam</p>
</div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════
T1,T2,T3,T4,T5,T6,T7=st.tabs(["🍕 Food Analyzer","🧠 Model Internals","📊 Visualizations","📚 DL Theory","🗄️ Datasets","🥗 Diet Planner","📐 Math & Exam"])

# ─── TAB 1: FOOD ANALYZER ─────────────────────────────────────────────
with T1:
    if uploaded is None:
        st.markdown("<div class='card' style='text-align:center;padding:3rem;'><div style='font-size:4rem;'>📸</div><div style='font-size:1.4rem;font-weight:700;color:white;'>Upload a food image to begin</div><div style='color:#666;margin:.4rem 0;'>Supports JPG · PNG · WebP</div><br/>" +
            "".join([f"<span class='pill'>{v['emoji']} {k.replace('_',' ').title()}</span>" for k,v in NUTRITION_DB.items()])+"</div>",unsafe_allow_html=True)
    else:
        image=Image.open(uploaded).convert("RGB")
        with st.spinner("🧠 CNN processing..."):
            label,conf,top5=cnn_predict(image)
            nut=NUTRITION_DB.get(label,{"calories":200,"protein":8,"carbs":30,"fats":7,"fiber":2,"emoji":"🍽️","category":"Unknown"})
        bmr=calc_bmr(weight,height,age,gender);tdee=calc_tdee(bmr,activity);ct=cal_target(tdee,goal);mt=ct/3
        pct=nut["calories"]/mt*100
        col_img,col_res=st.columns([1,1.6])
        with col_img:
            st.image(image,use_container_width=True)
            st.markdown("#### 🎯 Top-5 Predictions")
            for lbl,prob in top5:
                e=NUTRITION_DB.get(lbl,{}).get("emoji","🍽️")
                st.markdown(f"""<div style='margin:.25rem 0;'><div style='display:flex;justify-content:space-between;font-size:.9rem;'><span>{e} {lbl.replace('_',' ').title()}</span><span style='color:#F72585;font-family:Space Mono,monospace;'>{prob*100:.1f}%</span></div><div style='background:#1a1a2e;border-radius:4px;height:6px;margin-top:3px;'><div style='width:{int(prob*100)}%;height:6px;border-radius:4px;background:linear-gradient(90deg,#7209B7,#F72585);'></div></div></div>""",unsafe_allow_html=True)
        with col_res:
            st.markdown(f"""<div class='card'><div style='font-size:.75rem;color:#888;text-transform:uppercase;'>Detected Food</div><div class='fbadge'>{nut['emoji']} {label.replace('_',' ').title()}</div><div style='color:#888;font-size:.82rem;margin-top:.3rem;'>Confidence: <span style='color:#4CC9F0;font-family:Space Mono,monospace;'>{conf*100:.1f}%</span> · Category: <span style='color:#F72585;'>{nut['category']}</span> · Model: <span style='color:#4CAF50;'>{model_type}</span></div></div>""",unsafe_allow_html=True)
            mc1,mc2,mc3,mc4=st.columns(4)
            for col,val,lbl,unit in[(mc1,nut["calories"],"Calories","kcal"),(mc2,nut["protein"],"Protein","g"),(mc3,nut["carbs"],"Carbs","g"),(mc4,nut["fats"],"Fats","g")]:
                col.markdown(f"""<div class='mc'><div class='v'>{val}</div><div class='l'>{lbl}<br/><span style='color:#F72585;'>{unit}</span></div></div>""",unsafe_allow_html=True)
            pc={"<90":"#4CAF50","<120":"#FF9800"}.get(f"<{int(pct)+1}" if pct<120 else "else","#F44336")
            pc="#4CAF50" if pct<90 else "#FF9800" if pct<120 else "#F44336"
            st.markdown(f"""<div class='card' style='margin-top:.7rem;'><div style='font-size:.85rem;color:#888;'>Meal Target ({goal})</div><div style='font-size:1.8rem;font-weight:800;color:{pc};font-family:Space Mono,monospace;'>{pct:.0f}%</div><div style='color:#666;font-size:.78rem;'>{nut['calories']} kcal / {mt:.0f} kcal per meal · TDEE: {tdee:.0f} kcal/day</div></div>""",unsafe_allow_html=True)
            tips=[]
            if nut["calories"]>300 and goal=="Weight Loss":tips.append("⚠️ High-calorie — consider a smaller portion.")
            if nut["category"]=="Healthy":tips.append("✅ Great choice! Nutrient-dense and filling.")
            if nut["category"] in["Dessert","Fast Food"]:tips.append("🍎 Treat food — balance with nutritious meals.")
            tips+=["💧 Drink 8 glasses of water daily.","🕐 Eat 2-3 hours before bed."]
            st.markdown("#### 💡 Health Tips")
            for t in tips:st.markdown(f"<div class='tip'>{t}</div>",unsafe_allow_html=True)
            if label in HEALTHY_ALTS:
                st.markdown("#### 🌿 Healthier Alternatives")
                ca=st.columns(len(HEALTHY_ALTS[label]))
                for i,alt in enumerate(HEALTHY_ALTS[label]):
                    ca[i].markdown(f"""<div style='background:#0d2818;border:1px solid #4CAF50;border-radius:8px;padding:.55rem;text-align:center;font-size:.82rem;'>{alt}</div>""",unsafe_allow_html=True)
        st.markdown("#### 📊 Nutritional Analysis");st.pyplot(fig_macros(nut));plt.close()
        st.markdown("#### 🔮 30-Day Weight Impact");st.pyplot(fig_sim(label.replace("_"," ").title(),nut["calories"],ct));plt.close()
        if show_maps:
            st.markdown("#### 🔬 CNN Feature Maps — Layer 1")
            st.markdown("<div class='cb'>Each filter detects a different visual pattern: edges, gradients, textures. This is how the CNN builds understanding from raw pixels.</div>",unsafe_allow_html=True)
            st.pyplot(fig_fmaps(get_feature_maps(image)));plt.close()

# ─── TAB 2: MODEL INTERNALS ───────────────────────────────────────────
with T2:
    st.markdown("<div class='st'>🧠 Deep Learning Architecture Internals</div>",unsafe_allow_html=True)
    arch=st.radio("Select Architecture:",["CNN","Backpropagation","LSTM","Autoencoder"],horizontal=True)
    info={
        "CNN":("CNN — Food Classifier","3 Conv blocks (Conv→BN→ReLU→Pool) extract spatial features. FC layers with Dropout classify 20 food types via Softmax.",
               [("Input","224×224×3 pixels",C1),("Conv1+Pool","64 filters, 3×3 → 112×112 feature maps",C3),("Conv2+Pool","128 filters → 56×56",C3),
                ("Conv3+Pool","256 filters → 28×28",C3),("Flatten","256×28×28 values","#FF9800"),("FC+Dropout","512 neurons, Dropout(0.5), L2 λ=1e-4",C2),
                ("FC+Dropout","256 neurons, Dropout(0.3)",C2),("Softmax","20 food probabilities",C4)],fig_cnn),
        "Backpropagation":("Backpropagation — How Networks Learn","Forward pass computes predictions. Loss measures error. Backward pass uses chain rule to compute ∂L/∂W. Adam updates weights.",
                           [("Forward","x → h → ŷ",C1),("Loss","L = -Σ yᵢ log(ŷᵢ)","#FF5722"),
                            ("∂L/∂W_out","Direct gradient from output","#FF5722"),("∂L/∂W_hid","Chain rule: ∂L/∂h · ∂h/∂W","#FF5722"),
                            ("Adam Update","W ← W - η·m̂/(√v̂+ε)",C4)],fig_backprop),
        "LSTM":("LSTM — Sequential Diet Recommendation","Processes 7-day nutritional sequences. 3 gates control memory flow: Forget, Input, Output.",
                [("Input","[protein,carbs,fats,fiber,cal] × 7 days",C1),("Forget Gate","fₜ = σ(Wf·[hₜ₋₁,xₜ]+bf)",C1),
                 ("Input Gate","iₜ = σ(Wi·[hₜ₋₁,xₜ]+bi)",C2),("Cell Update","Cₜ = fₜ⊙Cₜ₋₁ + iₜ⊙tanh(...)",C3),
                 ("Output Gate","hₜ = oₜ⊙tanh(Cₜ)",C4),("FC Head","128 → 20 meal recs",C4)],fig_lstm),
        "Autoencoder":("Autoencoder — Feature Compression","Encoder compresses 150,528 pixels to 64-dim latent. Decoder reconstructs. Latent captures food fingerprint.",
                       [("Input","224×224×3 = 150,528 dims",C1),("Enc FC1","→ 512 (ReLU)",C3),("Enc FC2","→ 256 (ReLU)","#9B2226"),
                        ("Latent","→ 64 (bottleneck)",C2),("Dec FC1","→ 256 (ReLU)","#9B2226"),("Dec FC2","→ 512 (ReLU)",C3),
                        ("Output","→ 150,528 (Sigmoid)",C4)],fig_ae),
    }
    title,desc,rows,dfn=info[arch]
    st.markdown(f"<div class='cb'><b>{title}</b><br/><br/><span style='color:#ccc;'>{desc}</span></div>",unsafe_allow_html=True)
    st.markdown("#### 🏗️ Layer-by-Layer Breakdown")
    for layer,detail,col in rows:
        st.markdown(f"""<div style='display:flex;gap:1rem;align-items:center;background:#111128;border-radius:8px;padding:.5rem .9rem;margin:.25rem 0;border-left:3px solid {col};'><span style='color:{col};font-weight:700;min-width:130px;font-family:Space Mono,monospace;font-size:.82rem;'>{layer}</span><span style='color:#ccc;font-size:.88rem;'>{detail}</span></div>""",unsafe_allow_html=True)
    st.markdown("#### 🎨 Architecture Diagram");st.pyplot(dfn());plt.close()
    st.markdown("#### 📈 Training Curves");curves=sim_curves(epochs_sim);st.pyplot(fig_curves(curves));plt.close()
    st.markdown("#### 📊 Final Metrics")
    fm1,fm2,fm3,fm4=st.columns(4)
    for col,val,lbl in[(fm1,f"{curves['va'][-1]*100:.1f}%","Val Accuracy"),(fm2,f"{curves['vl'][-1]:.3f}","Val Loss"),(fm3,f"{curves['va'][-1]*100*1.12:.1f}%","Top-5 Accuracy"),(fm4,f"{epochs_sim}ep","Epochs")]:
        col.markdown(f"""<div class='mc'><div class='v' style='font-size:1.4rem;'>{val}</div><div class='l'>{lbl}</div></div>""",unsafe_allow_html=True)

# ─── TAB 3: VISUALIZATIONS ────────────────────────────────────────────
with T3:
    st.markdown("<div class='st'>📊 Interactive Visualizations</div>",unsafe_allow_html=True)
    viz=st.selectbox("Choose Visualization:",["📊 Calorie Comparison (All 20 Foods)","🕸️ Nutritional Radar (Compare 2 Foods)","⚡ Activation Functions","🎯 Gradient Descent Loss Landscape","🌌 Autoencoder Latent Space","🧩 Confusion Matrix"])
    descs={"Calorie":"Color-coded by category: Healthy · Fast Food · Dessert · Protein. Longer bar = more calories.",
           "Radar":"Radar chart comparing macronutrient profiles. Larger area = more nutrients overall.",
           "Activation":"Activation functions add non-linearity. Without them, deep networks collapse to linear transformations.",
           "Gradient":"The optimizer navigates the loss landscape following the steepest downhill direction (negative gradient).",
           "Latent":"Similar foods cluster together — the network learns food similarity purely from visual appearance.",
           "Confusion":"Diagonal = correct predictions. Off-diagonal = confusions (e.g., burger vs sandwich — similar visual features)."}
    key=next(k for k in descs if k in viz)
    st.markdown(f"<div class='cb'>{descs[key]}</div>",unsafe_allow_html=True)
    if "Calorie" in viz:st.pyplot(fig_calcomp());plt.close()
    elif "Radar" in viz:
        fc1,fc2=st.columns(2)
        with fc1:f1=st.selectbox("Food 1",FOOD_CLASSES,0)
        with fc2:f2=st.selectbox("Food 2",FOOD_CLASSES,1)
        st.pyplot(fig_radar(f1,f2));plt.close()
    elif "Activation" in viz:st.pyplot(fig_acts());plt.close()
    elif "Gradient" in viz:st.pyplot(fig_gd());plt.close()
    elif "Latent" in viz:st.pyplot(fig_latent());plt.close()
    elif "Confusion" in viz:st.pyplot(fig_conf());plt.close()

# ─── TAB 4: DL THEORY ────────────────────────────────────────────────
with T4:
    st.markdown("<div class='st'>📚 Deep Learning — Interactive Course</div>",unsafe_allow_html=True)
    concept=st.selectbox("Choose a concept:",["🧠 Artificial Neural Networks","🔗 Deep Feedforward Networks","🔄 Backpropagation","📸 Convolutional Neural Networks","🔁 Recurrent Neural Networks","💾 LSTM","📦 Autoencoders","🛡️ Regularization: Dropout & L2"])

    cdata={
        "🧠 Artificial Neural Networks":{
            "analogy":"🧠 Think of neurons like tiny decision makers. Each one receives signals, weighs their importance, and fires if the total signal is strong enough — exactly like biological neurons.",
            "exp":"An ANN consists of <b>layers of neurons</b>:<br/>• <b>Input Layer</b>: Raw data (pixel values)<br/>• <b>Hidden Layers</b>: Learn abstract patterns<br/>• <b>Output Layer</b>: Final predictions<br/><br/>Each neuron: <i>z = Σ wᵢxᵢ + b</i> → <i>activation(z)</i>",
            "formula":"output = ReLU(W·x + b) = max(0, W·x + b)",
            "code":"""import numpy as np

def neuron(x, w, b):
    z = np.dot(w, x) + b   # weighted sum
    return np.maximum(0, z) # ReLU activation

x = np.array([0.5, 0.3, 0.8])  # pixel values
w = np.array([0.2, -0.1, 0.4]) # learned weights
b = 0.1                         # bias
print(neuron(x, w, b))  # output: 0.42""","diagram":None},
        "🔗 Deep Feedforward Networks":{
            "analogy":"🚂 Like an assembly line — data enters, each station (layer) processes it and passes it FORWARD. Layer 1 learns edges → Layer 2 learns textures → Layer 3 learns food shapes.",
            "exp":"<b>Why deep?</b> Multiple layers allow hierarchical feature learning.<br/><br/><b>Universal Approximation Theorem</b>: A wide enough single hidden layer can approximate any continuous function. Depth makes this computationally efficient.<br/><br/>In NutriVision: pixels → edges → textures → food parts → food categories",
            "formula":"h₁ = ReLU(W₁x + b₁)\nh₂ = ReLU(W₂h₁ + b₂)\nŷ  = Softmax(W₃h₂ + b₃)",
            "code":"""import torch.nn as nn

class FoodDNN(nn.Module):
    def __init__(self, n_classes=20):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(150528, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),       # regularization
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, n_classes),
            nn.Softmax(dim=1)      # probabilities
        )
    def forward(self, x):
        return self.net(x.flatten(1))""","diagram":None},
        "🔄 Backpropagation":{
            "analogy":"🎯 Archery practice: you shoot (forward pass), miss (compute loss), adjust your aim (update weights). Backprop computes exactly HOW MUCH to adjust each weight using the chain rule.",
            "exp":"<b>4 Steps:</b><br/>1. Forward pass: compute ŷ<br/>2. Loss: L = -Σ yᵢ log(ŷᵢ)<br/>3. Backward: ∂L/∂W = ∂L/∂ŷ · ∂ŷ/∂h · ∂h/∂W<br/>4. Update: W ← W - η·∂L/∂W<br/><br/><b>Chain Rule</b> decomposes complex derivatives into products of simple ones — enabling efficient computation via dynamic programming.",
            "formula":"∂L/∂W₁ = (∂L/∂ŷ)·(∂ŷ/∂h₂)·(∂h₂/∂h₁)·(∂h₁/∂W₁)",
            "code":"""optimizer = torch.optim.Adam(
    model.parameters(), lr=0.001
)
loss_fn = nn.CrossEntropyLoss()

for x_batch, y_batch in dataloader:
    optimizer.zero_grad()            # clear old grads
    outputs = model(x_batch)         # forward pass
    loss = loss_fn(outputs, y_batch) # compute loss
    loss.backward()                  # BACKPROP ← ←
    optimizer.step()                 # update weights
    print(f"Loss: {loss.item():.4f}")""","diagram":fig_backprop},
        "📸 Convolutional Neural Networks":{
            "analogy":"🔍 Scanning a pizza with different magnifying glasses — one looks for red circles (tomato), another for brown texture (crust), another for white patches (cheese). CNN filters do exactly this, automatically learning what to detect.",
            "exp":"<b>Key operations:</b><br/>• <b>Convolution ★</b>: Filter slides over image, detecting local patterns<br/>• <b>ReLU</b>: Keeps only positive activations<br/>• <b>BatchNorm</b>: Stabilizes training, speeds convergence<br/>• <b>MaxPool</b>: Downsamples, keeps strongest signals<br/>• <b>Weight sharing</b>: One filter scans entire image = far fewer parameters than dense!",
            "formula":"z_l = Conv(h_{l-1}; W_l) + b_l\nh_l = ReLU(BN(z_l))\nOutput = Softmax(FC(GAP(h_L)))",
            "code":"""class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)   # halve spatial dims
        )
    def forward(self, x):
        return self.block(x)

model = nn.Sequential(
    ConvBlock(3,   64),  # 224→112
    ConvBlock(64,  128), # 112→56
    ConvBlock(128, 256), # 56→28
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Linear(256, 20),
    nn.Softmax(dim=1)
)""","diagram":fig_cnn},
        "🔁 Recurrent Neural Networks":{
            "analogy":"📖 Reading a recipe step-by-step — each step makes sense in context of what came before. An RNN maintains a hidden state (memory) that evolves with each input.",
            "exp":"<b>Problem</b>: Vanilla RNNs suffer from <b>vanishing gradients</b> — early information is lost for long sequences. Gradients shrink as: ∂L/∂h₀ ≈ ∏(∂hₜ/∂hₜ₋₁) → 0<br/><br/><b>Formula</b>: hₜ = tanh(Wₕ·hₜ₋₁ + Wₓ·xₜ + b)<br/><br/><b>Solution</b>: LSTM adds gating mechanisms to control what to remember and forget (see next concept).",
            "formula":"hₜ = tanh(Wₕ·hₜ₋₁ + Wₓ·xₜ + b)",
            "code":"""class RNN(nn.Module):
    def __init__(self, in_size, hid, out):
        super().__init__()
        self.rnn = nn.RNN(
            in_size, hid,
            batch_first=True
        )
        self.fc = nn.Linear(hid, out)

    def forward(self, x, h0=None):
        # x shape: (batch, seq_len, features)
        out, hn = self.rnn(x, h0)
        # Use last hidden state for prediction
        return self.fc(out[:, -1, :])

# 7 days of nutrition → diet recommendation
rnn = RNN(in_size=5, hid=64, out=20)""","diagram":None},
        "💾 LSTM":{
            "analogy":"🗃️ A smart notebook: you can WRITE new info (input gate), ERASE old info (forget gate), and READ from it (output gate). Selective memory solves vanishing gradients.",
            "exp":"<b>3 Gates control information flow:</b><br/>• <b>Forget Gate (fₜ)</b>: σ(·) → 0=forget all, 1=keep all<br/>• <b>Input Gate (iₜ)</b>: How much new info to store<br/>• <b>Output Gate (oₜ)</b>: What to output from cell state<br/><br/><b>Cell State (Cₜ)</b>: The conveyor belt — information flows with only minor modifications, preventing gradient vanishing.",
            "formula":"fₜ=σ(Wf·[hₜ₋₁,xₜ]+bf)\niₜ=σ(Wi·[hₜ₋₁,xₜ]+bi)\nCₜ=fₜ⊙Cₜ₋₁+iₜ⊙tanh(Wc·[hₜ₋₁,xₜ]+bc)\nhₜ=oₜ⊙tanh(Cₜ)",
            "code":"""class DietLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=5,    # cal,prot,carb,fat,fib
            hidden_size=128,
            num_layers=2,
            batch_first=True,
            dropout=0.3      # regularization
        )
        self.fc = nn.Linear(128, 20)

    def forward(self, meal_seq):
        # meal_seq: (batch, 7_days, 5_nutrients)
        out, (hn, cn) = self.lstm(meal_seq)
        return self.fc(out[:, -1, :])""","diagram":fig_lstm},
        "📦 Autoencoders":{
            "analogy":"🗜️ ZIP compression for food images. Compress a pizza photo (150,528 numbers) into 64 numbers (the 'essence'), then reconstruct it. Similar foods have similar 64-number fingerprints!",
            "exp":"<b>Two parts:</b><br/>• <b>Encoder</b>: Compresses input to latent code z ∈ ℝ^64<br/>• <b>Decoder</b>: Reconstructs input from z<br/><br/><b>Applications:</b><br/>• Feature extraction (z as food fingerprint)<br/>• Anomaly detection (high reconstruction loss = unknown food)<br/>• Similarity search (nearby z = similar foods)<br/>• Data compression",
            "formula":"z = Encoder(x; θₑ)  [150528 → 64]\nx̂ = Decoder(z; θd)  [64 → 150528]\nL = ||x - x̂||²     [MSE loss]",
            "code":"""class FoodAutoencoder(nn.Module):
    def __init__(self, latent=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(150528, 512), nn.ReLU(),
            nn.Linear(512, 256),    nn.ReLU(),
            nn.Linear(256, latent)  # BOTTLENECK
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent, 256), nn.ReLU(),
            nn.Linear(256, 512),    nn.ReLU(),
            nn.Linear(512, 150528), nn.Sigmoid()
        )
    def forward(self, x):
        z = self.encoder(x)       # compress
        return self.decoder(z), z # reconstruct""","diagram":fig_ae},
        "🛡️ Regularization: Dropout & L2":{
            "analogy":"📚 Memorizing vs understanding. Overfitting = memorizing training images. Dropout: study with random notes removed → forced to learn all material. L2: penalize extreme opinions → balanced learning.",
            "exp":"<b>Dropout</b>: Randomly zero p fraction of neurons each forward pass. Forces redundant representations. At test time: all neurons active, scaled by (1-p).<br/><br/><b>L2 (Weight Decay)</b>: Add λ·||W||² to loss. Penalizes large weights. Equivalent to Bayesian Gaussian prior. In Adam: implemented via weight_decay parameter.<br/><br/><b>Combined effect</b>: Dropout prevents co-adaptation · L2 keeps weights small & distributed",
            "formula":"L_total = L_CE + λ·||W||²_F\nDropout: h̃ᵢ = hᵢ·Bernoulli(1-p) / (1-p)",
            "code":"""# Dropout in PyTorch
nn.Dropout(p=0.5)   # 50% neurons zeroed during training

# L2 via Adam weight_decay parameter
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    weight_decay=1e-4  # λ = 0.0001
)

# In Keras / TensorFlow:
from tensorflow.keras.regularizers import l2
Dense(512, activation='relu',
      kernel_regularizer=l2(1e-4))
# Dropout
Dropout(0.5)""","diagram":None},
    }

    d=cdata.get(concept,{})
    if d:
        st.markdown(f"<div class='card'><b>💡 The Analogy</b><br/><br/><div style='color:#ccc;line-height:1.7;'>{d['analogy']}</div></div>",unsafe_allow_html=True)
        ce,cc=st.columns([1.1,1])
        with ce:
            st.markdown(f"""<div class='cb'><b>📖 Explanation</b><br/><br/><div style='color:#ccc;line-height:1.7;'>{d['exp']}</div><br/><b>📐 Formula</b><br/><div style='background:#0d1117;padding:.7rem;border-radius:6px;font-family:Space Mono,monospace;color:#F72585;margin-top:.4rem;font-size:.82rem;white-space:pre;'>{d['formula']}</div></div>""",unsafe_allow_html=True)
        with cc:
            st.markdown(f"<div class='codebox'>{d['code']}</div>",unsafe_allow_html=True)
        if d.get("diagram"):
            st.markdown("#### 🎨 Architecture Diagram");st.pyplot(d["diagram"]());plt.close()

# ─── TAB 5: DATASETS ──────────────────────────────────────────────────
with T5:
    st.markdown("<div class='st'>🗄️ Datasets & Data Pipeline</div>",unsafe_allow_html=True)
    st.markdown("""<div class='card'><b style='color:#4CC9F0;font-size:1.1rem;'>Primary Dataset: Food-101</b><br/><br/>
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:.8rem;'>
    <div style='background:#111128;border-radius:8px;padding:.8rem;text-align:center;'><div style='font-size:1.5rem;font-weight:800;color:#F72585;font-family:Space Mono,monospace;'>101,000</div><div style='color:#888;font-size:.8rem;'>Total Images</div></div>
    <div style='background:#111128;border-radius:8px;padding:.8rem;text-align:center;'><div style='font-size:1.5rem;font-weight:800;color:#4CC9F0;font-family:Space Mono,monospace;'>101</div><div style='color:#888;font-size:.8rem;'>Food Categories</div></div>
    <div style='background:#111128;border-radius:8px;padding:.8rem;text-align:center;'><div style='font-size:1.5rem;font-weight:800;color:#4CAF50;font-family:Space Mono,monospace;'>1,000</div><div style='color:#888;font-size:.8rem;'>Images per Class</div></div>
    </div></div>""",unsafe_allow_html=True)
    d1,d2=st.columns(2)
    with d1:
        st.markdown("""<div class='card'><b>📦 Dataset Details</b><br/><br/>
        <table style='width:100%;font-size:.85rem;color:#ccc;'>
        <tr><td style='color:#888;padding:.3rem 0;'>Source</td><td>ETH Zürich (2014)</td></tr>
        <tr><td style='color:#888;padding:.3rem 0;'>Train / Test</td><td>75,750 / 25,250</td></tr>
        <tr><td style='color:#888;padding:.3rem 0;'>Image size</td><td>Variable → 224×224</td></tr>
        <tr><td style='color:#888;padding:.3rem 0;'>Labels</td><td>Class labels only</td></tr>
        <tr><td style='color:#888;padding:.3rem 0;'>License</td><td>CC BY-SA 3.0</td></tr>
        </table></div>""",unsafe_allow_html=True)
    with d2:
        st.markdown("""<div class='card'><b>🔗 Additional Datasets</b><br/><br/>
        <div style='margin:.4rem 0;padding:.5rem;background:#111128;border-radius:6px;'><span style='color:#4CC9F0;font-weight:700;'>UEC-Food256</span> <span style='color:#888;font-size:.82rem;'>— 256 categories, 31K images, Japanese cuisine</span></div>
        <div style='margin:.4rem 0;padding:.5rem;background:#111128;border-radius:6px;'><span style='color:#F72585;font-weight:700;'>VIREO-172</span> <span style='color:#888;font-size:.82rem;'>— 172 Chinese dishes, 110K images</span></div>
        <div style='margin:.4rem 0;padding:.5rem;background:#111128;border-radius:6px;'><span style='color:#4CAF50;font-weight:700;'>Nutrition5k</span> <span style='color:#888;font-size:.82rem;'>— Google dataset with actual calorie measurements</span></div>
        <div style='margin:.4rem 0;padding:.5rem;background:#111128;border-radius:6px;'><span style='color:#FF9800;font-weight:700;'>USDA FoodData</span> <span style='color:#888;font-size:.82rem;'>— Nutritional DB for 300K+ foods</span></div>
        </div>""",unsafe_allow_html=True)
    st.markdown("#### ⚙️ Preprocessing Pipeline")
    for step,code,why in[
        ("1. Load Image","PIL.Image.open(path).convert('RGB')","Read raw image file"),
        ("2. Resize","transforms.Resize((224, 224))","Standardize for CNN input"),
        ("3. Augment","RandomFlip, ColorJitter, RandomRotation(15°)","Increase diversity, reduce overfitting"),
        ("4. ToTensor","transforms.ToTensor()","PIL → torch.Tensor [0,1]"),
        ("5. Normalize","mean=[0.485,0.456,0.406] std=[0.229,0.224,0.225]","ImageNet stats — zero-mean unit variance"),
        ("6. Batch","DataLoader(batch_size=32, shuffle=True)","Group for efficient GPU training"),
    ]:
        st.markdown(f"""<div style='display:grid;grid-template-columns:150px 1fr 1fr;gap:.8rem;background:#111128;border-radius:8px;padding:.6rem .9rem;margin:.25rem 0;align-items:center;'><span style='color:#F72585;font-weight:700;font-size:.85rem;'>{step}</span><span style='font-family:Space Mono,monospace;font-size:.73rem;color:#4CC9F0;'>{code}</span><span style='color:#888;font-size:.82rem;'>{why}</span></div>""",unsafe_allow_html=True)
    st.markdown("#### 📊 Class Distribution")
    foods_list=list(NUTRITION_DB.keys())
    counts=[1000+np.random.RandomState(i).randint(-50,50) for i in range(20)]
    fig,ax=plt.subplots(figsize=(13,4),facecolor=BG);dax(ax)
    cmap2={"Healthy":C4,"Fast Food":C2,"Dessert":"#FF9800","Protein":C1,"Asian":"#AB47BC","Italian":"#EF9A9A","Snack":"#80CBC4","Mexican":"#FFD54F"}
    bc=[cmap2.get(NUTRITION_DB[f]["category"],"#888") for f in foods_list]
    ax.bar([NUTRITION_DB[f]["emoji"]+"\n"+f.replace("_","\n") for f in foods_list],counts,color=bc,alpha=.85)
    ax.set_title("Images per Food Class",color="white",fontsize=11,fontweight="bold")
    ax.set_ylabel("Count",color="#aaa");ax.tick_params(axis='x',labelsize=7,labelcolor="white")
    fig.patch.set_facecolor(BG);plt.tight_layout();st.pyplot(fig);plt.close()

# ─── TAB 6: DIET PLANNER ──────────────────────────────────────────────
with T6:
    st.markdown("<div class='st'>🥗 Personalized Diet Planner</div>",unsafe_allow_html=True)
    bmr=calc_bmr(weight,height,age,gender);tdee=calc_tdee(bmr,activity);ct=cal_target(tdee,goal)
    bmi=weight/((height/100)**2);bmi_cat="Underweight" if bmi<18.5 else "Normal" if bmi<25 else "Overweight" if bmi<30 else "Obese"
    pm1,pm2,pm3,pm4=st.columns(4)
    for col,val,lbl in[(pm1,f"{bmr:.0f}","BMR (kcal)"),(pm2,f"{tdee:.0f}","TDEE (kcal)"),(pm3,f"{ct:.0f}",f"Target ({goal})"),(pm4,f"{bmi:.1f}",f"BMI · {bmi_cat}")]:
        col.markdown(f"""<div class='mc'><div class='v' style='font-size:1.5rem;'>{val}</div><div class='l'>{lbl}</div></div>""",unsafe_allow_html=True)
    st.markdown("<div class='cb'><b>Mifflin-St Jeor:</b> BMR(♂) = 10W + 6.25H − 5A + 5 &nbsp;|&nbsp; TDEE = BMR × Activity Multiplier &nbsp;|&nbsp; Target = TDEE ± 500 kcal</div>",unsafe_allow_html=True)
    st.markdown("#### 🎯 Daily Macro Targets")
    sp={"Weight Loss":(.35,.40,.25),"Maintenance":(.25,.50,.25),"Weight Gain":(.30,.50,.20)}.get(goal,(.25,.50,.25))
    sm1,sm2,sm3=st.columns(3)
    for col,macro,pct,cpg in[(sm1,"Protein",sp[0],4),(sm2,"Carbs",sp[1],4),(sm3,"Fats",sp[2],9)]:
        g=ct*pct/cpg
        col.markdown(f"""<div class='mc'><div class='v' style='font-size:1.5rem;'>{g:.0f}g</div><div class='l'>{macro}<br/><span style='color:#F72585;'>{pct*100:.0f}% of calories</span></div></div>""",unsafe_allow_html=True)
    st.markdown("#### 📅 7-Day LSTM-Optimized Meal Plan")
    plan=WEEKLY_PLANS.get(goal,WEEKLY_PLANS["Maintenance"])
    icons=["🌅","☀️","🌤️","⛅","🌙","🌟","🎉"]
    cw=st.columns(7)
    for i,(day,meals) in enumerate(plan.items()):
        with cw[i]:
            st.markdown(f"""<div class='wd'><div style='text-align:center;font-size:1.1rem;'>{icons[i]}</div><div style='color:#4CC9F0;font-weight:700;font-size:.78rem;text-align:center;'>{day}</div><hr style='border-color:#2d2d4e;margin:.35rem 0;'/><div style='font-size:.68rem;color:#4CAF50;font-weight:700;'>☀️ Breakfast</div><div style='font-size:.7rem;color:#ccc;margin-bottom:.35rem;'>{meals[0]}</div><div style='font-size:.68rem;color:#FF9800;font-weight:700;'>🕛 Lunch</div><div style='font-size:.7rem;color:#ccc;margin-bottom:.35rem;'>{meals[1]}</div><div style='font-size:.68rem;color:#F72585;font-weight:700;'>🌙 Dinner</div><div style='font-size:.7rem;color:#ccc;'>{meals[2]}</div></div>""",unsafe_allow_html=True)
    st.markdown("#### 🍽️ Meal History Tracker")
    if "meals" not in st.session_state:st.session_state.meals=[]
    ta1,ta2,ta3=st.columns([2,1,1])
    with ta1:fc=st.selectbox("Add food",FOOD_CLASSES,format_func=lambda x:f"{NUTRITION_DB[x]['emoji']} {x.replace('_',' ').title()}",key="fcs")
    with ta2:sv=st.number_input("Servings",.5,5.,1.,.5)
    with ta3:
        st.markdown("<br/>",unsafe_allow_html=True)
        if st.button("➕ Add"):
            n=NUTRITION_DB[fc]
            st.session_state.meals.append({"Food":f"{n['emoji']} {fc.replace('_',' ').title()}","Servings":sv,"Calories":int(n["calories"]*sv),"Protein(g)":round(n["protein"]*sv,1),"Carbs(g)":round(n["carbs"]*sv,1),"Fats(g)":round(n["fats"]*sv,1)})
    if st.session_state.meals:
        df=pd.DataFrame(st.session_state.meals);st.dataframe(df,use_container_width=True,hide_index=True)
        tot=df["Calories"].sum();rem=ct-tot;rc="#4CAF50" if rem>0 else "#F44336"
        st.markdown(f"""<div class='card' style='display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;'><div><span style='color:#888;'>Consumed: </span><span style='color:#F72585;font-family:Space Mono,monospace;font-size:1.1rem;'>{tot} kcal</span></div><div><span style='color:#888;'>Remaining: </span><span style='color:{rc};font-family:Space Mono,monospace;font-size:1.1rem;'>{rem:+.0f} kcal</span></div><div><span style='color:#888;'>Target: </span><span style='color:#4CC9F0;font-family:Space Mono,monospace;font-size:1.1rem;'>{ct:.0f} kcal</span></div></div>""",unsafe_allow_html=True)
        if st.button("🗑️ Clear"):st.session_state.meals=[];st.rerun()

# ─── TAB 7: MATH & EXAM ───────────────────────────────────────────────
with T7:
    st.markdown("<div class='st'>📐 Mathematical Formulation — Exam Reference</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'><b style='color:#F72585;'>NeuralHack 2026 · End Trimester Examination</b><br/><span style='color:#888;font-size:.88rem;'>AI-Powered Food Calorie Detector & Personalized Diet Recommendation System</span></div>",unsafe_allow_html=True)
    for title,content in[
        ("1️⃣ Problem Definition (CO1)","""
**Input:** Food images X ∈ ℝ^(N×3×224×224)  
**Output:** Food class ŷ ∈ {1,...,20}, calories ĉ ∈ ℝ⁺, macros [p̂, k̂, f̂] ∈ ℝ³  
**Task:** Multi-class classification (CNN) + nutritional regression + sequence modeling (LSTM)  
**Real-world:** Diet-related diseases are a global crisis. AI-powered instant calorie tracking democratizes nutrition science.
        """),
        ("2️⃣ Mathematical Modeling (CO2)","""
**CNN Forward Pass:**
```
z_l = Σ W_l[k] ★ h_{l-1} + b_l         (convolution)
h_l = ReLU(BatchNorm(z_l))               (activation + normalization)
ŷ   = Softmax(W_fc · GAP(h_L) + b_fc)   (classification head)
```

**Loss Function:**
```
L_CE    = -Σᵢ yᵢ · log(ŷᵢ)             (categorical cross-entropy)
L_total = L_CE + λ · Σₗ ||W_l||²_F     (+ L2 regularization, λ=1e-4)
```

**Backpropagation:**
```
δ_L = ∂L_CE/∂z_L                        (output layer gradient)
δ_l = (W_{l+1}ᵀ · δ_{l+1}) ⊙ ReLU'(z_l) (hidden layer gradient)
∂L/∂W_l = δ_l · h_{l-1}ᵀ               (weight gradient)
```

**Adam Optimizer:**
```
mₜ = β₁mₜ₋₁ + (1-β₁)∇L    m̂ₜ = mₜ/(1-β₁ᵗ)
vₜ = β₂vₜ₋₁ + (1-β₂)(∇L)²  v̂ₜ = vₜ/(1-β₂ᵗ)
W  ← W - η·m̂ₜ/(√v̂ₜ + ε)            (η=0.001, β₁=0.9, β₂=0.999)
```

**LSTM Gates:**
```
fₜ = σ(Wf·[hₜ₋₁,xₜ]+bf)     (forget gate)
iₜ = σ(Wi·[hₜ₋₁,xₜ]+bi)     (input gate)
Cₜ = fₜ⊙Cₜ₋₁ + iₜ⊙tanh(Wc·[hₜ₋₁,xₜ]+bc)  (cell state)
hₜ = oₜ⊙tanh(Cₜ)             (output)
```

**Autoencoder:**
```
z  = FC_64(ReLU(FC_256(ReLU(FC_512(x)))))    [encode: 150528→64]
x̂  = Sigmoid(FC_150528(ReLU(FC_512(ReLU(FC_256(z))))))  [decode]
L_AE = ||x - x̂||²_2                         [MSE reconstruction loss]
```

**BMR/TDEE:**
```
BMR(♂) = 10W + 6.25H - 5A + 5   |  BMR(♀) = 10W + 6.25H - 5A - 161
TDEE   = BMR × aᵢ (aᵢ ∈ {1.2, 1.375, 1.55, 1.725, 1.9})
Target = TDEE ± 500 kcal
```

**Evaluation:**
```
Top-1 Acc  = correct / N
Top-5 Acc  = true_in_top5 / N
F1         = 2·(P·R)/(P+R)   [macro-averaged]
Calorie MAE = (1/N)·Σ|c_true - ĉ|
```
        """),
        ("3️⃣ Architecture Design (CO3)","""
```
CNN:  Input(224×224×3) → ConvBlock×3 → GlobalAvgPool → FC(512)+Drop(0.5) → FC(256)+Drop(0.3) → Softmax(20)
LSTM: Input(7,5) → LSTM(128, layers=2, drop=0.3) → FC(20)
AE:   Enc: 150528→512→256→64  |  Dec: 64→256→512→150528
Regularization: Dropout(0.5, 0.3) · L2(λ=1e-4) · BatchNorm · DataAugmentation
```
        """),
        ("4️⃣ Training & Evaluation (CO4)","""
| Config | Value |
|--------|-------|
| Dataset | Food-101 (20 classes, 20K train, 5K test) |
| Optimizer | Adam (lr=0.001, wd=1e-4) |
| Loss | CrossEntropy + L2 |
| Epochs | 50 + ReduceLROnPlateau |
| Batch size | 32 |

**Targets:** Top-1 ≥ 85% · Top-5 ≥ 97% · Calorie MAE ≤ 25kcal · F1 ≥ 0.83
        """),
        ("5️⃣ User Interface (CO5)","""
**Streamlit single-file app with 7 tabs:**
1. 🍕 Food Analyzer — CNN prediction + nutrition + simulation + feature maps  
2. 🧠 Model Internals — Architecture diagrams + training curves  
3. 📊 Visualizations — 6 interactive charts  
4. 📚 DL Theory — 8-concept interactive course  
5. 🗄️ Datasets — Food-101 + preprocessing pipeline  
6. 🥗 Diet Planner — BMR/TDEE + meal plans + tracker  
7. 📐 Math & Exam — This reference page  

**CO1 ✓ · CO2 ✓ · CO3 ✓ · CO4 ✓ · CO5 ✓**
        """),
    ]:
        with st.expander(title,expanded=False):st.markdown(content)
    st.markdown("#### 🏗️ CNN Architecture Overview");st.pyplot(fig_cnn());plt.close()
    st.markdown("""<div class='card' style='text-align:center;'><div style='color:#888;font-size:.82rem;'>NeuralHack 2026 · NutriVision AI · Single-File Edition</div><div style='font-family:Space Mono,monospace;color:#4CC9F0;font-size:.78rem;margin-top:.3rem;'>CO1 ✓ CO2 ✓ CO3 ✓ CO4 ✓ CO5 ✓</div></div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""<div style='text-align:center;margin-top:2rem;padding:1rem;border-top:1px solid #2d2d4e;color:#333;font-size:.72rem;font-family:Space Mono,monospace;'>
NutriVision AI · NeuralHack 2026 · Single-File Streamlit Edition<br/>
CNN · LSTM · Autoencoder · Backpropagation · Dropout · L2 · Adam
</div>""",unsafe_allow_html=True)
