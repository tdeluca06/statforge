# statforge
StatForge - Extrapolate college football statistics in order to predict future events

Users will need to obtain their own API keys from collegefootballdata.com and
create a variable in their environment containing the API key from the terminal:
On Linux/Mac or a Linux subsystem:
export API_KEY="your API key"
On windows:
set API_KEY=your_api_key

We are creating software to calculate the betting line on a college football game using the home and away team’s SRS values with the formula (int HomeSRS + 2.5) - int AwaySRS. Store this value in a “calculatedSRSLine” variable of type integer, write the calculated values to an excel file, and compare the sportsbook’s line with the calculated SRS line using a formula like sportsbook - SRS to determine probability of bet hitting. We should only collect data from D1 NCAA teams, disregarding all of the other SRS scores from other schools.

