from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# Function to scrape team performance
# W - Wins, L - Losses, W/L% - Win-loss percentage, GB - Games Behind, PS/G - Points per Games,
# PA/G - Opponent Points per game, SRS - Simple Rating System
# SRS is basically a team rating that takes into account average point differential and strength of schedule
# The SRS rating is denoted by points above.below average, where zero is average
def scrape_NBA_team_data(years=[2017, 2018]):
    final_df = pd.DataFrame(columns=["Year", "Team", "W", "L",
                                     "W/L%", "GB", "PS/G", "PA/G",
                                     "SRS", "Playoffs",
                                     "Losing_season"])

    # Loop through each year
    for y in years:
        # NBA season to scrape
        year = y

        # URL to scrape, notice f string:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

        # Collect HTML data
        html = urlopen(url)

        # Beautiful soup object from HTML
        soup = BeautifulSoup(html, "html.parser")

        # getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

        # Column headers
        headers = titles[1:titles.index("SRS") + 1]

        # Exclude first set of column headers
        titles = titles[titles.index("SRS") + 1:]

        # Row titles
        try:
            row_titles = titles[0:titles.index("Eastern Conference")]
        except:
            row_titles = titles
        # remove the non-teams from this list
        for i in headers:
            row_titles.remove(i)
        row_titles.remove("Western Conference")
        divisions = ["Atlantic Division", "Central Division",
                     "Southeast Division", "Northwest Division",
                     "Pacific Division", "Southwest Division",
                     "Midwest Division"]
        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print("no division:", d)

        # Extract all data from rows (avoid first row)
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
                      for i in range(len(rows))]
        # Remove empty elements
        team_stats = [e for e in team_stats if e != []]
        # Important rows
        team_stats = team_stats[0:len(row_titles)]

        # Add team name to each row in team_stats
        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)

        # Add team and year columns to headers
        headers.insert(0, "Team")
        headers.insert(0, "Year")

        # Dataframe with all extracted info
        year_standings = pd.DataFrame(team_stats, columns=headers)

        # Add a column to dataframe to indicate playoff appearance
        year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
        # Remove * from team names
        year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
        # Add losing season indicator (win % < .5)
        year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]

        # Append new dataframe to final_df
        final_df = final_df.append(year_standings)

    # print final_df
    print(final_df.info)
    # export to csv
    final_df.to_csv("NBATeamsData.csv", index=False)


scrape_NBA_team_data(years = [1990, 1991, 1992, 1993, 1994,
                              1995, 1996, 1997, 1998, 1999,
                              2000, 2001, 2002, 2003, 2004,
                              2005, 2006, 2007, 2008, 2009,
                              2010, 2011, 2012, 2013, 2014,
                              2015, 2016, 2017, 2018, 2019,
                              2020])