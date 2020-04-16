This is a nice text in overview

<div id="wrapper-research">
    <table>
        <thead>
            <tr>
                <th>Index</th>
                <th>Options</th>
            </tr>
        </thead>
    {{#each researches}}
        <tr>
            <td>{{researchIndex}}</td>
            <td><a href="/show/{{researchIndex}}">Show</a></td>
        </tr>
    {{/each}}
</div>