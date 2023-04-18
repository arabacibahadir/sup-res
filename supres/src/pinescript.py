def pinescript_code(p_ticker, selected_tf, res_above, res_below) -> str:
    """
    Writes resistance and support lines to a file called pinescript.txt.
    """
    pinescript_lines = []
    lines_sma = (
        f"//@version=5\nindicator('Sup-Res {p_ticker} {selected_tf}',"
        f" overlay=true)\n"
        "plot(ta.sma(close, 50), title='50 SMA', color=color.new(color.blue, 0), linewidth=1)\n"
        "plot(ta.sma(close, 100), title='100 SMA', color=color.new(color.purple, 0), linewidth=1)\n"
        "plot(ta.sma(close, 200), title='200 SMA', color=color.new(color.red, 0), linewidth=1)\n"
    )

    for line_res in res_above[:10]:
        if line_res == 0:
            continue
        lr = f'hline({line_res}, title="Lines", color=color.red, linestyle=hline.style_solid, linewidth=1)'
        pinescript_lines.append(lr)

    for line_sup in res_below[:10]:
        if line_sup == 0:
            continue
        ls = f'hline({line_sup}, title="Lines", color=color.green, linestyle=hline.style_solid, linewidth=1)'
        pinescript_lines.append(ls)
    lines = "\n".join(map(str, pinescript_lines))
    # Create a new file that called pinescript.txt and write the lines_sma and lines variables to the file
    with open("/pinescript.txt", "w") as pine:
        pine.writelines(lines_sma + lines)

        def ichimoku():  # read ichimoku_cloud.txt and write it to pinescript.txt
            with open("pinescripts/ichimoku_cloud.txt") as ichimoku_read:
                # write a blank line to separate the ichimoku cloud from the support and resistance lines
                pine.write("\n")
                pine.writelines(ichimoku_read.read())

        def daily_levels():
            with open("pinescripts/daily_levels.txt") as d_levels:
                pine.write("\n")
                pine.writelines(d_levels.read())

        ichimoku()
        daily_levels()
    return lines
