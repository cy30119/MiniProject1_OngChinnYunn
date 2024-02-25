from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d
from bokeh.embed import components
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd

#Create a login-required function to create plot for stock data visualization
@login_required  
def stock_visualizations(request):
   
   #Load combined stock dataset
   df = pd.read_csv(r"C:\Users\Chinnyunn_Ong\Downloads\MiniProject1_OngChinnYunn\dataset\combined_stock_data.csv", parse_dates=["Date"])
   
   #Convert the columns to floats
   df["CloseDELL"] = df["CloseDELL"].replace(",","",regex=True).astype(float)
   df["CloseS&P500"] = df["CloseS&P500"].replace(",","",regex=True).astype(float)

   #Prepare the data
   source = ColumnDataSource(df)

   #Create first plot about monthly price comparison between Dell and S&P 500
   p1 = figure(title="Monthly Price Comparison", 
               x_axis_label="Year", 
               y_axis_label="Dell Price", 
               x_axis_type="datetime")
    
   #Manually set the y-range for Dell to use more vertical space
   p1.y_range = Range1d(start=df["CloseDELL"].min(), end=df["CloseDELL"].max())
    
   p1.line("Date","CloseDELL",
           source=source,
           legend_label="Dell",
           line_width=3,
           color="blue")
    
   #Add secondary y-axis
   p1.extra_y_ranges = {"S&P500":Range1d(start=df["CloseS&P500"].min(),end=df["CloseS&P500"].max())}
    
   p1.add_layout(LinearAxis(y_range_name="S&P500", axis_label="S&P 500 Price"), "right")
   
   p1.line("Date", "CloseS&P500", 
           source=source, 
           legend_label="S&P 500", 
           line_width=2, 
           color="green", 
           y_range_name="S&P500")
    
   #Customize legend
   p1.legend.location = "top_left"

   #Calculate monthly percentage change
   df["Dell_percent_change"] = df["CloseDELL"].pct_change() * 100
   df["SP500_percent_change"] = df["CloseS&P500"].pct_change() * 100

   #Prepare the data
   source = ColumnDataSource(df)

   #Create second plot about monthly percentage change comparison between Dell and S&P 500
   p2 = figure(title="Monthly Percentage Change Comparison",
                x_axis_label="Date",
                y_axis_label="% Change",
                x_axis_type="datetime",
                height=600,
                width=600)
    
   p2.vbar(x="Date",
           top="Dell_percent_change",
           width=0.9,
           source=source,
           color="blue",
           legend_label="Dell")
   
   p2.vbar(x="Date", 
           top="SP500_percent_change",
           width=0.9,
           source=source,
           color="green",
           legend_label="S&P 500")

   #Customize legend 
   p2.legend.location = "top_left"

   #Sort dates
   df.sort_values("Date", ascending=True, inplace=True)

   df["Dell_monthly_return"] = df["CloseDELL"].pct_change()
   df["SP500_monthly_return"] = df["CloseS&P500"].pct_change()

   #Calculate cumulative returns
   df["Dell_cum_returns"] = (1 + df["Dell_monthly_return"]).cumprod() - 1
   df["SP500_cum_returns"] = (1 + df["SP500_monthly_return"]).cumprod() - 1

   #Prepare the data
   source = ColumnDataSource(df)

   #Create third plot about cumulative returns comparison between Dell and S&P 500
   p3 = figure(title="Cumulative Returns Comparison",
                x_axis_label="Date",
                y_axis_label="Cumulative Returns",
                x_axis_type="datetime")
   
   p3.varea(x="Date", y1=0, y2="Dell_cum_returns",
            source=source,
            legend_label = "Dell",
            fill_alpha=0.2,
            fill_color="blue")
    
   p3.varea(x="Date", y1=0, y2="SP500_cum_returns",
            source=source,
            legend_label = "S&P 500",
            fill_alpha=0.2,
            fill_color="green")
    
   #Customize legend
   p3.legend.location = "top_left"
   
   #Generate components to pass to template
   script1, div1 = components(p1)
   script2, div2 = components(p2)
   script3, div3 = components(p3)

   context = {"script1":script1, 
              "div1":div1,
              "description1":"This plot provides a monthly price comparison between Dell and S&P 500 over time. The blue line represents Dell while the green line represents the S&P 500 index. It is evident that Dell stock price shows a significant increase in 2022, surpassing the performance of the S&P 500 index, suggesting a strong performance from Dell during this period.",
              "script2":script2, 
              "div2":div2,
              "description2":"This plot displays the monthly percentage change of Dell and S&P 500. The bars represent the month-over-month percentage change in value for each. Dell which represented by blue bars appears to have more pronounced fluctuations compared to the S&P 500 index, suggesting higher volatility in Dell stock price.",
               "script3":script3, 
               "div3":div3,
               "description3":"This plot shows the cumulative returns for Dell stock compared to the S&P 500 index. The shaded areas under the lines represent the value of the investment over time. By early 2024, Dell cumulative returns have substantially outpaced the S&P 500, indicating that an investment in Dell would generate higher return than an investment in the broader market index over this time frame."}
   
   #Pass components yo template
   return render(request, "BokehDjango/base.html", context)