Const CheminBase2 As String = "/path/to/project/back"
Const CheminBase3 As String = "/path/to/project/back"


Private Sub Workbook_Open()
    Dim cheminFichier As String
    ' Spécifiez le chemin complet du fichier que vous souhaitez vérifier
    cheminFichier = "back/bash/dismiss_macros.txt"
        
    ' Vérifiez si le fichier existe
    If Dir(cheminFichier) <> "" Then
        ' Le fichier existe
        GoTo FinMacro
    Else
        ' Le fichier n'existe pas
        Dim commandResult As String
        Dim commandToRun As String
        commandToRun = "sh """ & ThisWorkbook.Path & "/back/bash/pull.sh"""
        commandResult = AppleScriptTask("ShellExScript.scpt", "ShellEx", commandToRun)
        If VerifierFichier() = True Then
            ' Exécuter le code souhaité ici
            commandResult = AppleScriptTask("ShellExScript.scpt", "ShellEx", "sh """ & ThisWorkbook.Path & "/back/bash/write_changes.sh""")
            CopierValeurs
        Else
            ' Ne rien faire
        End If
        MsgBox "Fichier ouvert"
    End If
        
    ' Code à exécuter après la vérification du fichier
FinMacro:
    ' Fin de la macro
End Sub

Function VerifierFichier() As Boolean
    Dim cheminFichier As String
    Dim Numero As String
    
    ' Spécifiez le chemin complet du fichier que vous souhaitez vérifier
    cheminFichier = ThisWorkbook.Path & "/back/bash/changes.txt"
    
    ' Ouvrir le fichier texte et lire la première ligne
    Open cheminFichier For Input As #1
    Line Input #1, Numero
    Close #1
    
    ' Vérifier si le numéro est égal à 1
    If Numero = "1" Then
        ' Exécuter le code ici
        VerifierFichier = True
    Else
        VerifierFichier = False
    End If
End Function

Sub ReloadPage()
    ThisWorkbook.RefreshAll
    Dim filePath As String
    filePath = ThisWorkbook.FullName
    ThisWorkbook.Close SaveChanges:=False
    Workbook.Open filePath
End Sub


Sub CopierValeurs()
    Dim wbSource As Workbook
    Set wbSource = Workbooks.Open(ThisWorkbook.Path & "/back/BD.xlsx")  ' Fichier source = fichier actif
    
    Dim wsSource As Worksheet
    Set wsSource = wbSource.Worksheets("BD") ' Feuille source
    
    Dim wbCible As Workbook
    Set wbCible = ThisWorkbook ' Fichier source = fichier actif
    
    Dim wsCible As Worksheet
    Set wsCible = wbCible.Worksheets("BD") ' Feuille cible
    
    wsCible.Range("A1").Resize(wsSource.UsedRange.Rows.Count, _
        wsSource.UsedRange.Columns.Count).Value = wsSource.UsedRange.Value ' Copie les valeurs de la source dans la cible
        
    wbSource.Close SaveChanges:=False

End Sub

Private Sub Workbook_AfterSave(ByVal Success As Boolean)
    Dim cheminFichier As String
    
    ' Spécifiez le chemin complet du fichier que vous souhaitez vérifier
    cheminFichier = "back/bash/dismiss_macros.txt"
    
    ' Vérifiez si le fichier existe
    If Dir(cheminFichier) <> "" Then
        ' Le fichier existe
        GoTo FinMacro
    Else
        ' Le fichier n'existe pas
        Dim commandResult As String
        Dim commandToRun As String
        commandToRun = "sh """ & ThisWorkbook.Path & "/back/bash/after_save.sh"""
        commandResult = AppleScriptTask("ShellExScript.scpt", "ShellEx", commandToRun)
    End If
    
    ' Code à exécuter après la vérification du fichier
FinMacro:
    ' Fin de la macro
    MsgBox "Sauvegarde effectuée"
End Sub
