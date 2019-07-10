update NYSCR_raw set labelText = 'Due Date:' where labelText like '%Due%' or labelText like '%End%';
update NYSCR_raw set labelText = 'Company:' where labelText like '%Agency%';
update DASNY_raw set resultText = substring(resultText, 0, CHARINDEX(' ', resultText)) where labelText like '%Due%';
update GOVUK_raw set [resultText] = substring([resultText], 5, 2) + '/' + substring([resultText], 2, 2) + '/' + substring([resultText], 8, 4) where [labelText] like '%Closing%' or [labelText] like '%Publication%';
update RFPDB_raw set resultText = substring(resultText,0, 11) where labelText = 'endDate';