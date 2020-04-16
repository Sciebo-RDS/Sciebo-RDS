This is a nice text in overview

<div id="wrapper-research">
    <table>
        <thead>
            <tr>
                <th>Index</th>
                <th>Options</th>
            </tr>
        </thead>
    {{#each studies}}
        <tr>
            <td>{{researchIndex}}</td>
            <td><a href="edit/{{researchIndex}}">Show</a>, <a href="#">Delete</a></td>
        </tr>
    {{/each}}
</div>