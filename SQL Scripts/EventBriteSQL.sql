
insert into event_master_table(Title, shortSummary, longSummary, URL, eventStart, eventEnd, publishDate, insertDate, status, onlineEvent, address, category, site, Expired)
select [Title], [shortSummary], [longSummary], [URL], [eventStart], [eventEnd], [publishDate], [insertDate], [status], [onlineEvent], [address], [category], 'eventBrite', 'No'
from eventBrite_raw
WHERE eventBrite_raw.[Title] not in(select Title from event_master_table);

truncate table eventBrite_raw;

update event_master_table set Expired = 'Yes' where eventEnd < GETDATE();

delete from event_current_table where eventEnd < getdate();
update event_current_table set recent = 'Old';

insert into event_current_table(title, shortSummary, URL, eventStart, eventEnd, publishDate, insertDate, address, category, site, recent, masterTableID)
select distinct Title, shortSummary, URL, eventStart, eventEnd, publishDate, insertDate, address, category, site, 'New', eventID
from event_master_table
WHERE event_master_table.Title not in(select Title from event_current_table) and event_master_table.eventEnd > GETDATE();

