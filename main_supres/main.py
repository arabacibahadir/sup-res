import os
import time
from dataclasses import dataclass
import pandas as pd
import pandas_ta.momentum as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import delete_file
import historical_data


@dataclass
class Values:
    ticker_csv: str
    selected_timeframe: str

    def __post_init__(self):
        self.ticker_csv = self.ticker_csv.upper()
        self.selected_timeframe = self.selected_timeframe.lower()


class Supres(Values):
    @staticmethod
    def main(ticker_csv, selected_timeframe, candle_count=254):
        print(f"Start main function in {time.perf_counter() - perf} seconds\n"
              f"{ticker_csv} data analysis in progress.")
        df = pd.read_csv(ticker_csv, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=candle_count,
                         keep_default_na=False)
        df = df.iloc[::-1]
        df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
        df = pd.concat([df, df.tail(1)], axis=0, ignore_index=True)
        df.dropna(inplace=True)
        historical_hightimeframe = (historical_data.Client.KLINE_INTERVAL_1DAY,
                                    historical_data.Client.KLINE_INTERVAL_3DAY)
        historical_lowtimeframe = (historical_data.Client.KLINE_INTERVAL_1MINUTE,
                                   historical_data.Client.KLINE_INTERVAL_3MINUTE,
                                   historical_data.Client.KLINE_INTERVAL_5MINUTE,
                                   historical_data.Client.KLINE_INTERVAL_15MINUTE,
                                   historical_data.Client.KLINE_INTERVAL_30MINUTE,
                                   historical_data.Client.KLINE_INTERVAL_1HOUR,
                                   historical_data.Client.KLINE_INTERVAL_2HOUR,
                                   historical_data.Client.KLINE_INTERVAL_4HOUR,
                                   historical_data.Client.KLINE_INTERVAL_6HOUR,
                                   historical_data.Client.KLINE_INTERVAL_8HOUR,
                                   historical_data.Client.KLINE_INTERVAL_12HOUR)

        # Sma, Rsi, Macd, Fibonacci variables
        def indicators(ma_length1=10, ma_length2=50, ma_length3=100) -> tuple[tuple, tuple, tuple, tuple]:
            """
            This function takes in three integer arguments, and returns a dataframe with three columns,
            each containing the moving average of the closing price for the given length.
            
            :param ma_length1: The length of the first moving average, defaults to 10 (optional)
            :param ma_length2: The length of the second moving average, defaults to 50 (optional)
            :param ma_length3: The length of the third moving average, defaults to 100 (optional)
            """
            dfsma = df[:-1]
            sma_1 = tuple((dfsma.ta.sma(ma_length1)))
            sma_2 = tuple((dfsma.ta.sma(ma_length2)))
            sma_3 = tuple((dfsma.ta.sma(ma_length3)))
            rsi_tuple = tuple((ta.rsi(df['close'][:-1])))
            return sma_1, sma_2, sma_3, rsi_tuple

        sma1, sma2, sma3, rsi = indicators()
        support_list, resistance_list, fibonacci_uptrend, fibonacci_downtrend, pattern_list = [], [], [], [], []
        support_above, support_below, resistance_below, resistance_above, x_date = [], [], [], [], ''
        fibonacci_multipliers = (0.236, 0.382, 0.500, 0.618, 0.705, 0.786, 0.886, 1.13)
        # Chart settings
        legend_color = "#D8D8D8"
        chart_color = "#E7E7E7"
        background_color = "#E7E7E7"
        support_line_color = "LightSeaGreen"
        resistance_line_color = "MediumPurple"
        # Add a watermark to the plot
        watermark_layout = (dict(name="draft watermark", text="twitter.com/sup_res", textangle=-30, opacity=0.15,
                                 font=dict(color="black", size=100), xref="paper", yref="paper", x=0.5, y=0.3,
                                 showarrow=False))
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                            vertical_spacing=0, row_width=[0.1, 0.1, 0.8])

        def support(candle_value, candle_index, before_candle_count, after_candle_count) -> (bool | None):
            """
            If the price of the asset is increasing for the last before_candle_count and decreasing for
            the last after_candle_count, then return True. Otherwise, return False
            :param candle_value: The price data for the asset
            :param candle_index: The index of the first bar in the support
            :param before_candle_count: The number of bars back you want to look
            :param after_candle_count: The number of bars in the second trend
            :return: True if the price of the price is supported by the previous low price, False if it is not
            """
            try:
                for current_value in range(candle_index - before_candle_count + 1, candle_index + 1):
                    if candle_value.low[current_value] > candle_value.low[current_value - 1]:
                        return False
                for current_value in range(candle_index + 1, candle_index + after_candle_count + 1):
                    if candle_value.low[current_value] < candle_value.low[current_value - 1]:
                        return False
                return True
            except KeyError:
                pass

        def resistance(candle_value, candle_index, before_candle_count, after_candle_count) -> (bool | None):
            """
            If the price of the stock is increasing for the last before_candle_count and decreasing for the last
            after_candle_count, then return True. Otherwise, return False
            :param candle_value: The price data for the asset
            :param candle_index: The index of the first candlestick in the resistance
            :param before_candle_count: The number of candlesticks back you want to analyze
            :param after_candle_count: The number of candlesticks after the can
            :return: True if the price has been increasing for the last n1 periods and decreasing for the n2 periods
            """
            try:
                for current_value in range(candle_index - before_candle_count + 1, candle_index + 1):
                    if candle_value.high[current_value] < candle_value.high[current_value - 1]:
                        return False
                for current_value in range(candle_index + 1, candle_index + after_candle_count + 1):
                    if candle_value.high[current_value] > candle_value.high[current_value - 1]:
                        return False
                return True
            except KeyError:
                pass

        def fibonacci_pricelevels(high_price, low_price) -> tuple[list, list]:
            """
            Uptrend Fibonacci Retracement Formula =>
            Fibonacci Price Level = High Price - (High Price - Low Price)*Fibonacci Level
            :param high_price: High price for the current price level
            :param low_price: Low price for the period
            """
            for multiplier in fibonacci_multipliers:
                retracement_levels_uptrend = low_price + (high_price - low_price) * multiplier
                fibonacci_uptrend.append(retracement_levels_uptrend)
                retracement_levels_downtrend = high_price - (high_price - low_price) * multiplier
                fibonacci_downtrend.append(retracement_levels_downtrend)
            return fibonacci_uptrend, fibonacci_downtrend

        def candlestick_patterns() -> list:
            """
            Takes in a dataframe and returns a list of candlestick patterns found in the dataframe
            """
            from candlestick import candlestick
            nonlocal df
            df = candlestick.inverted_hammer(df, target='inverted_hammer')
            df = candlestick.hammer(df, target='hammer')
            df = candlestick.doji(df, target='doji')
            df = candlestick.bearish_harami(df, target='bearish_harami')
            df = candlestick.bearish_engulfing(df, target='bearish_engulfing')
            df = candlestick.bullish_harami(df, target='bullish_harami')
            df = candlestick.bullish_engulfing(df, target='bullish_engulfing')
            df = candlestick.dark_cloud_cover(df, target='dark_cloud_cover')
            df = candlestick.dragonfly_doji(df, target='dragonfly_doji')
            df = candlestick.hanging_man(df, target='hanging_man')
            df = candlestick.gravestone_doji(df, target='gravestone_doji')
            df = candlestick.morning_star(df, target='morning_star')
            df = candlestick.morning_star_doji(df, target='morning_star_doji')
            df = candlestick.piercing_pattern(df, target='piercing_pattern')
            df = candlestick.star(df, target='star')
            df = candlestick.shooting_star(df, target='shooting_star')
            df.replace({True: 'pattern_found'}, inplace=True)  # Dodge boolean 'True' output

            def pattern_find_func(pattern_row, t=0, pattern_find=None) -> list:
                """
                The function takes in a dataframe and a list of column names. It then iterates through the
                list of column names and checks if the column name is in the dataframe. If it is, it adds
                the column name to a list and adds the date of the match to another list
                """
                if pattern_find is None:
                    pattern_find = []
                for col in df.columns:
                    pattern_find.append(col)
                for pattern in pattern_row:
                    if pattern == 'pattern_found':
                        # even pattern, odd date
                        pattern_list.append(pattern_find[t])
                        pattern_list.append(pattern_row['date'].strftime('%b-%d-%y'))
                    t += 1
                return pattern_list

            # Loop through the dataframe and find the pattern in the dataframe
            for item in range(-3, -30, -1):
                pattern_find_func(df.iloc[item])
            return pattern_list

        def sensitivity(sens=3) -> tuple[list, list]:
            """
            Find the support and resistance levels for a given asset
            sensitivity:1 is recommended for daily charts or high frequency trade scalping
            :param sens: sensitivity parameter default:2, level of detail 1-2-3 can be given to function
            """
            for sens_row in range(3, len(df) - 1):
                if support(df, sens_row, 3, sens):
                    support_list.append((sens_row, df.low[sens_row]))
                if resistance(df, sens_row, 3, sens):
                    resistance_list.append((sens_row, df.high[sens_row]))
            return support_list, resistance_list

        def check_lines() -> tuple[list, list]:
            """
            Check if the support and resistance lines are above or below the latest close price.
            """
            # Find support and resistance levels
            # Check if the support is below the latest close. If it is, it is appending it to the list
            # support_below. If it isn't, it is appending it to the list resistance_below.
            all_support_list = tuple(map(lambda sup1: sup1[1], support_list))
            all_resistance_list = tuple(map(lambda res1: res1[1], resistance_list))
            latest_close = tuple(df['close'])[-1]
            for support_line in all_support_list:  # Find closes
                if support_line < latest_close:
                    support_below.append(support_line)
                else:
                    resistance_below.append(support_line)
            # Check if the price is above the latest close price. If it is, it is appending it to the
            # resistance_above list. If it is not, it is appending it to the support_above list.
            for resistance_line in all_resistance_list:
                if resistance_line > latest_close:
                    resistance_above.append(resistance_line)
                else:
                    support_above.append(resistance_line)
            return list(all_support_list), list(all_resistance_list)

        def legend_candle_patterns() -> None:
            fig.add_trace(go.Scatter(
                y=[support_list[0]], name="----------------------------------------", mode="markers",
                marker=dict(color=legend_color, size=14)))
            fig.add_trace(go.Scatter(
                y=[support_list[0]], name="Latest Candlestick Patterns", mode="markers",
                marker=dict(color=legend_color, size=14)))
            for pat1 in range(1, len(pattern_list), 2):  # Candlestick patterns
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"{pattern_list[pat1]} -> {pattern_list[pat1 - 1]}", mode="lines",
                    marker=dict(color=legend_color, size=10)))

        def levels() -> tuple[list, list]:
            # Check if the support level is empty. If it is, it appends the minimum value of the low
            # column to the list.
            if len(support_below) == 0:
                support_below.append(df.low.min())
            # Check if the resistance level is empty. If it is, it appends the minimum value of the high
            # column to the list.
            if len(resistance_above) == 0:
                resistance_above.append(df.high.max())
            # Compute the Fibonacci sequence for the numbers in the range of the last element of the
            # resistance_above list and the last element of the support_below list.
            return fibonacci_pricelevels(resistance_above[-1], support_below[-1])

        def create_candlestick_plot() -> None:
            fig.add_trace(go.Candlestick(x=df['date'][:-1].dt.strftime(x_date),
                                         name="Candlestick",
                                         text=df['date'].dt.strftime(x_date),
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close']), row=1, col=1)
            fig.update_layout(annotations=[watermark_layout])

        def add_volume_subplot() -> None:
            fig.add_trace(go.Bar(x=df['date'][:-1].dt.strftime(x_date), y=df['Volume USDT'], name="Volume USDT",
                                 showlegend=False), row=2, col=1)

        def add_rsi_subplot() -> None:
            fig.add_trace(go.Scatter(x=df['date'][:-1].dt.strftime(x_date), y=rsi, name="RSI",
                                     showlegend=False), row=3, col=1)
            fig.add_hline(y=30, name="RSI lower band", line=dict(color='red', width=1), line_dash='dash', row=3, col=1)
            fig.add_hline(y=70, name="RSI higher band", line=dict(color='red', width=1), line_dash='dash', row=3, col=1)
            fig.add_hrect(y0=30, y1=70, line_width=0, fillcolor="gray", opacity=0.2, row=3, col=1)

        def draw_support(c=0) -> None:
            """
            Draws the support lines and adds annotations to the chart.
            """
            while True:
                if c > len(support_list) - 1:
                    break
                # Support lines
                fig.add_shape(type='line', x0=support_list[c][0] - 1, y0=support_list[c][1],
                              x1=len(df) + 25,
                              y1=support_list[c][1], line=dict(color=support_line_color, width=2))
                # Support annotations
                fig.add_annotation(x=len(df) + 7, y=support_list[c][1], text=str(support_list[c][1]),
                                   font=dict(size=15, color=support_line_color))
                c += 1

        def draw_resistance(c=0) -> None:
            """
            Draws the resistance lines and adds annotations to the chart.
            """
            while True:
                if c > len(resistance_list) - 1:
                    break
                # Resistance lines
                fig.add_shape(type='line', x0=resistance_list[c][0] - 1, y0=resistance_list[c][1],
                              x1=len(df) + 25,
                              y1=resistance_list[c][1], line=dict(color=resistance_line_color, width=1))
                # Resistance annotations
                fig.add_annotation(x=len(df) + 20, y=resistance_list[c][1], text=str(resistance_list[c][1]),
                                   font=dict(size=15, color=resistance_line_color))
                c += 1

        def legend_texts() -> None:
            fig.add_trace(go.Scatter(
                y=[support_list[0]], name=f"Resistances    ||   Supports", mode="markers+lines",
                marker=dict(color=resistance_line_color, size=10)))
            str_price_len = 3
            sample_price = df['close'][0]
            if sample_price < 1:
                str_price_len = len(str(sample_price))

            def legend_support_resistance_values(temp=0) -> None:
                blank = " " * (len(str(sample_price)) + 1)
                differ = len(float_resistance_above) - len(float_support_below)
                try:
                    if differ < 0:
                        for i in range(abs(differ)):
                            float_resistance_above.extend([0])
                    if differ > 0:
                        for i in range(abs(differ)):
                            float_support_below.extend([0])
                    for _ in range(max(len(float_resistance_above), len(float_support_below))):
                        if float_resistance_above[temp] == 0:  # This is for legend alignment
                            legend_supres = f"{float(float_resistance_above[temp]):.{str_price_len - 1}f}{blank}     " \
                                            f"||   {float(float_support_below[temp]):.{str_price_len - 1}f}"
                        else:
                            legend_supres = f"{float(float_resistance_above[temp]):.{str_price_len - 1}f}       " \
                                            f"||   {float(float_support_below[temp]):.{str_price_len - 1}f}"
                        fig.add_trace(go.Scatter(
                            y=[support_list[0]],
                            name=legend_supres,
                            mode="lines",
                            marker=dict(color=legend_color, size=10)))
                        if temp != 14:
                            temp += 1
                        else:
                            break
                except IndexError:
                    pass

            def text_and_indicators() -> None:
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"github.com/arabacibahadir/sup-res", mode="markers",
                    marker=dict(color=legend_color, size=0)))
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"-------  twitter.com/sup_res  --------", mode="markers",
                    marker=dict(color=legend_color, size=0)))
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"Indicators", mode="markers", marker=dict(color=legend_color, size=14)))
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"RSI         : {int(rsi[-1])}", mode="lines",
                    marker=dict(color=legend_color, size=10)))
                # Add SMA10, SMA50, and SMA100 to the chart and legend
                fig.add_trace(go.Scatter(x=df['date'].dt.strftime(x_date), y=sma1,
                                         name=f"SMA10     : {float(sma1[-1]):.{str_price_len}f}",
                                         line=dict(color='#5c6cff', width=3)))
                fig.add_trace(go.Scatter(x=df['date'].dt.strftime(x_date), y=sma2,
                                         name=f"SMA50     : {float(sma2[-1]):.{str_price_len}f}",
                                         line=dict(color='#950fba', width=3)))
                fig.add_trace(go.Scatter(x=df['date'].dt.strftime(x_date), y=sma3,
                                         name=f"SMA100   : {float(sma3[-1]):.{str_price_len}f}",
                                         line=dict(color='#a69b05', width=3)))
                fig.add_trace(go.Scatter(
                    y=[support_list[0]], name=f"-- Fibonacci Uptrend | Downtrend --", mode="markers",
                    marker=dict(color=legend_color, size=0)))

            def legend_fibonacci() -> None:
                # Add a line to the legend for each Fibonacci level
                mtp = len(fibonacci_multipliers) - 1
                for _ in fibonacci_uptrend:
                    fig.add_trace(go.Scatter(
                        y=[support_list[0]],
                        name=f"Fib {fibonacci_multipliers[mtp]:.3f} "
                             f": {float(fibonacci_uptrend[mtp]):.{str_price_len}f} "
                             f"| {float(fibonacci_downtrend[mtp]):.{str_price_len}f} ",
                        mode="lines",
                        marker=dict(color=legend_color, size=10)))
                    mtp -= 1

            legend_support_resistance_values()
            text_and_indicators()
            legend_fibonacci()
            # Candle patterns for HTF
            if selected_timeframe in historical_hightimeframe:
                legend_candle_patterns()

        def chart_updates() -> None:
            fig.update_layout(title=str(f"{historical_data.ticker} {selected_timeframe.upper()} Chart"),
                              hovermode='x', dragmode="zoom",
                              paper_bgcolor=background_color, plot_bgcolor=chart_color, xaxis_rangeslider_visible=False,
                              legend=dict(bgcolor=legend_color, font=dict(size=11)), margin=dict(t=30, l=0, b=0, r=0))
            fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
            fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)

        def save():
            """
            Saves the image and html file of the plotly chart, then it tweets the image and text
            """
            if not os.path.exists("../main_supres/images"):
                os.mkdir("images")
            image = \
                f"../main_supres/images/{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{historical_data.ticker}.jpeg"
            fig.write_image(image, width=1920, height=1080)  # Save image for tweet
            fig.write_html(
                f"../main_supres/images/"
                f"{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{historical_data.ticker}.html",
                full_html=False, include_plotlyjs='cdn')
            text_image = f"#{historical_data.ticker} #{historical_data.symbol_data.get('baseAsset')} " \
                         f"{selected_timeframe} Support and resistance levels \n " \
                         f"{df['date'].dt.strftime('%b-%d-%Y')[candle_count]} #crypto #btc"

            def for_tweet() -> None:
                """
                Takes a screenshot of a chart, then tweets it with a caption.
                """
                import tweet
                tweet.send_tweet(image, text_image)
                while tweet.is_image_tweet().text != text_image:
                    time.sleep(1)
                    if tweet.is_image_tweet().text != text_image:
                        resistance_above_nonzero = list(filter(lambda x: x != 0, float_resistance_above))
                        support_below_nonzero = list(filter(lambda x: x != 0, float_support_below))
                        tweet.api.update_status(status=f"#{historical_data.ticker}  "
                                                       f"{df['date'].dt.strftime('%b-%d-%Y')[candle_count]} "
                                                       f"{selected_timeframe} Support and resistance levels"
                                                       f"\nRes={resistance_above_nonzero[:7]} \n"
                                                       f"Sup={support_below_nonzero[:7]}",
                                                in_reply_to_status_id=tweet.is_image_tweet().id)
                    break
            # for_tweet()

        def pinescript_code() -> str:
            """
            It takes resistance and support lines, and writes them to a file called pinescript.txt.
            """
            pinescript_lines = []
            lines_sma = f"//@version=5\nindicator('Sup-Res {historical_data.ticker} {selected_timeframe}'," \
                        f" overlay=true)\n" \
                        "plot(ta.sma(close, 50), title='50 SMA', color=color.new(color.blue, 0), linewidth=1)\n" \
                        "plot(ta.sma(close, 100), title='100 SMA', color=color.new(color.purple, 0), linewidth=1)\n" \
                        "plot(ta.sma(close, 200), title='200 SMA', color=color.new(color.red, 0), linewidth=1)\n"

            for line_res in float_resistance_above[:10]:
                if line_res == 0:
                    continue
                lr = f"hline({line_res}, title=\"Lines\", color=color.red, linestyle=hline.style_solid, linewidth=1)"
                pinescript_lines.append(lr)

            for line_sup in float_support_below[:10]:
                if line_sup == 0:
                    continue
                ls = f"hline({line_sup}, title=\"Lines\", color=color.green, linestyle=hline.style_solid, linewidth=1)"
                pinescript_lines.append(ls)
            lines = '\n'.join(map(str, pinescript_lines))
            # Create a new file called pinescript.txt and write the lines_sma and lines variables to the file
            file = open("../main_supres/pinescript.txt", "w")
            file.write(lines_sma + lines)
            file.close()
            return lines

        sensitivity()
        check_lines()
        if selected_timeframe in historical_hightimeframe:
            candlestick_patterns()
            x_date = '%b-%d-%y'
        elif selected_timeframe in historical_lowtimeframe:
            x_date = '%H:%M %d-%b'
        create_candlestick_plot()
        add_volume_subplot()
        add_rsi_subplot()
        levels()
        float_resistance_above = list(map(float, sorted(resistance_above + resistance_below)))
        float_support_below = list(map(float, sorted(support_below + support_above, reverse=True)))
        draw_support()
        draw_resistance()
        legend_texts()
        chart_updates()
        # save()
        pinescript_code()
        print(f"Completed execution in {time.perf_counter() - perf} seconds")
        return fig.show(id='the_graph', config={'displaylogo': False})


if __name__ == "__main__":
    os.chdir("../main_supres")  # Change the directory to the main_supres folder
    file_name = historical_data.file_name
    try:
        perf = time.perf_counter()
        historical_data.hist_data()
        if os.path.isfile(file_name):  # Check .csv file is there or not
            print(f"{file_name} downloaded and created.")
            Supres.main(file_name, historical_data.time_frame)
            delete_file.remove(file_name)
        else:
            raise print("One or more issues caused the download to fail. "
                        "Make sure you typed the filename correctly.")

    except KeyError:
        delete_file.remove(file_name)
        raise KeyError("Key error, algorithm issue")
