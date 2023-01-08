from plugins.send_to_slack import send_to_slack
from plugins.transform.read_transform import run_transform
import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style('dark_grid')
import os
from dotenv import load_dotenv

HOME = os.getcwd()
load_dotenv(HOME + '/.env')

def run():
    file_bytes = "output/sales_daily_report.png"

    # GMV per Products
    data_product = run_transform(group_by='product').sort_values('total_price', ascending=False).head(3)
    # GMV per Month
    data_month = run_transform(group_by='month')

    fig1 =  plt.figure(figsize=(16,8))
    # Sales per Products
    plt.subplot(121)
    plt.title('Sales by Product')
    plt.bar(data_product['Product'], data_product['total_price'])
    plt.xlabel('Top 3 Products')
    plt.ylabel('Total Sales (USD)')

    # Sales per Month  
    plt.subplot(122)
    plt.title('Sales by Month')
    plt.bar(data_month['Order Date'].dt.month.astype(str), data_month['total_price'])
    plt.xlabel('Month')
    plt.ylabel('Total Sales (USD)')

    # Save graph ke image png
    fig1.savefig(file_bytes, bbox_inches='tight')

    # send graph to slack channel
    message = "This is the Revenue per product performance"
    channel = "channel"

    send_to_slack.execute(message, channel, file_bytes)


if __name__ == '__main__':
    run()