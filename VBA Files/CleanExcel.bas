Attribute VB_Name = "Module1"
Sub Make_Links_jobs()

    Dim rng As Range
    Set rng = ActiveSheet.Range("c2")
    
    Do While rng.Value <> ""
        rng.Parent.Hyperlinks.Add Anchor:=rng, Address:=rng.Offset(0, 7).Value, SubAddress:= _
            rng.Offset(0, 7).Value, TextToDisplay:=rng.Value
                
        Set rng = rng.Offset(1)
    Loop

End Sub

Sub jobsFormat()

    Columns("A:A").EntireColumn.AutoFit
    Columns("B:B").EntireColumn.AutoFit
    Columns("C:C").ColumnWidth = 43.09
    Columns("C:C").Select
    With Selection
        .WrapText = True
    End With
    Columns("D:D").EntireColumn.AutoFit
    Columns("E:E").EntireColumn.AutoFit
    Columns("E:E").ColumnWidth = 32.09
    Columns("E:E").Select
    With Selection
        .WrapText = True
    End With
    Columns("F:F").EntireColumn.AutoFit
    Columns("G:G").EntireColumn.AutoFit
    Columns("H:H").EntireColumn.AutoFit
    Columns("I:I").EntireColumn.AutoFit
    Columns("I:I").ColumnWidth = 11.64
    Columns("I:I").Select
    With Selection
        .WrapText = True
    End With
    Columns("L:L").EntireColumn.AutoFit
    Columns("M:M").EntireColumn.AutoFit
    Columns("N:N").EntireColumn.AutoFit
    Columns("K:K").ColumnWidth = 14.73
    Range("B1").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.Borders(xlDiagonalDown).LineStyle = xlNone
    Selection.Borders(xlDiagonalUp).LineStyle = xlNone
    With Selection.Borders(xlEdgeLeft)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeBottom)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeRight)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlInsideVertical)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlInsideHorizontal)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    Columns("L:L").Select
    Selection.Delete Shift:=xlToLeft
    Range("A1").Select
End Sub

Sub eventsFormat()

    Columns("C:C").ColumnWidth = 37
    Columns("C:C").Select
    With Selection
        .WrapText = True
    End With
    Columns("B:B").EntireColumn.AutoFit
    Columns("A:A").EntireColumn.AutoFit
    Selection.ColumnWidth = 55.64
    Columns("D:D").ColumnWidth = 40
    Columns("D:D").Select
    With Selection
        .WrapText = True
    End With
    Columns("F:F").EntireColumn.AutoFit
    Columns("G:G").EntireColumn.AutoFit
    Columns("H:H").EntireColumn.AutoFit
    Columns("I:I").EntireColumn.AutoFit
    Columns("J:J").ColumnWidth = 21.82
    Columns("J:J").Select
    With Selection
        .WrapText = True
    End With
    Columns("K:K").EntireColumn.AutoFit
    Columns("L:L").EntireColumn.AutoFit
    Columns("M:M").EntireColumn.AutoFit
    Columns("N:N").EntireColumn.AutoFit
      Range("B1").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.Borders(xlDiagonalDown).LineStyle = xlNone
    Selection.Borders(xlDiagonalUp).LineStyle = xlNone
    With Selection.Borders(xlEdgeLeft)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeTop)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeBottom)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlEdgeRight)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlInsideVertical)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    With Selection.Borders(xlInsideHorizontal)
        .LineStyle = xlContinuous
        .ColorIndex = 0
        .TintAndShade = 0
        .Weight = xlThin
    End With
    Range("A1").Select
End Sub


Sub Make_Links_events()

    Dim rng As Range
    Set rng = ActiveSheet.Range("c2")
    
    Do While rng.Value <> ""
        rng.Parent.Hyperlinks.Add Anchor:=rng, Address:=rng.Offset(0, 2).Value, SubAddress:= _
            rng.Offset(0, 2).Value, TextToDisplay:=rng.Value
                
        Set rng = rng.Offset(1)
    Loop

End Sub


Sub DoSomething()
    Sheets(1).Select
    Call Make_Links_jobs
    Call jobsFormat
    Sheets(2).Select
    Call Make_Links_events
    Call eventsFormat
    Sheets(3).Select
    Call Make_Links_jobs
    Call jobsFormat
    Sheets(4).Select
    Call Make_Links_events
    Call eventsFormat
    Sheets(7).Select
    Call Make_Links_events
    Call eventsFormat
    Sheets(8).Select
    Call Make_Links_events
    Call eventsFormat
    Sheets(9).Select
    Call Make_Links_jobs
    Call jobsFormat
    Sheets(10).Select
    Call Make_Links_jobs
    Call jobsFormat
    Sheets(11).Select
    Call Make_Links_jobs
    Call jobsFormat
    Sheets(9).Select
End Sub





