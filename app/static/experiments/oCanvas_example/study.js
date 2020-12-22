var study = {

    start: function(params, next) {
        params['results'].push(['trial','block','stimId','category','response','accuracy','rt'])

        /*   initialize   */
        space = oCanvas.create({
            canvas: study.initCanvas(),
            background: 'rgba(190,190,190,1)',
            // origin: { x: "center", y: "center" },
        })
        study.initElements(params)

        x = new Date().getTime()
        rt = 0
        response = null
        acc = null
        trial = 0
        block = 0
        block_order = study.generateBlockOrder(params['objects'], params['labels']) // <-- initialize the first block order (you'll do this every block)

        correctCategory = block_order[trial][1]
        study.initStim(block_order[trial][0])
        space.scenes.load('selection')


        /*   define event logic   */
        responseBtn.bind('click tap', function () {
            rt = new Date().getTime() - x

            space.scenes.unload('selection')
            stimulus.remove()

            params['results'].push([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], correctCategory, response, acc, rt]) // pulled this variable from the main template
            trial += 1
            if (trial == block_order.length) {
                trial = 0
                block += 1
                if (block == params['n_blocks']) {
                    space.destroy(space)
                    document.getElementById('main').innerHTML = ''
                    next()
                } else {
                    block_order = study.generateBlockOrder(params['objects'], params['labels'])
                }
            }

            setTimeout( function () {
                space.scenes.load('selection')
                study.initStim(block_order[trial][0])
                correctCategory = block_order[trial][1]
                x = new Date().getTime()
            }, 200)

        })

        console.log('started study')
    },


    initElements: function (params) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        /*   Response Phase of Trial   */
        responseBtn = space.display.rectangle({
            x: centerX,
            y: centerY + 200,
            origin: { x: "center", y: "center" },// align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })
        responseBtn.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" },// align: 'center',
                font: "bold 25px sans-serif",
                text: 'Im done here',
                fill: "rgba(255,255,255,1)",
                zIndex: "front",
            })
        )

        instructionsTxt = space.display.text({
            x: centerX,
            y: centerY + 120,
            origin: { x: "center", y: "center" }, align: 'center',
            align: "center",
            font: "bold 25px sans-serif",
            text: "Study this item",
            fill: "rgba(0,0,0,1)",
            zIndex: "front",
        })

        space.scenes.create('selection', function () {
            this.add(responseBtn)
            this.add(instructionsTxt)
        })
    },


    initStim: function (image) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        stimulus = space.display.image({
            x: centerX,
            y: centerY - 100,
            origin: { x: "center", y: "center" }, align: 'center',
            image: image,
        })
        space.addChild(stimulus)
    },


    generateBlockOrder: function (objects, labels) {
        let block = []
        idx = study.shuffle([...Array(labels.length).keys()]) // from ben @ https://stackoverflow.com/a/10050831

        for (let i of idx) {
            block.push([objects[i], labels[i]])
        }

        return block
    },


    shuffle: function (array) { // from mike bostok @ https://bost.ocks.org/mike/shuffle/
        var m = array.length, t, i;

        // While there remain elements to shuffle…
        while (m) {

            // Pick a remaining element…
            i = Math.floor(Math.random() * m--);

            // And swap it with the current element.
            t = array[m];
            array[m] = array[i];
            array[i] = t;
        }

        return array;
    
    },


    initCanvas: function () {
        canvas = document.createElement('canvas', {id: 'canvas', style: 'position:absolute;'})
        document.getElementById('main').appendChild(canvas)
        
        var ctx = canvas.getContext('2d');
        // ctx.lineWidth = 2;
        ctx.canvas.width  = window.innerWidth - 20;
        ctx.canvas.height = window.innerHeight - 20;

        window.addEventListener('resize', function () {
            space.width = window.innerWidth - 20;
            space.height = window.innerHeight - 20;
        }, false);

        return canvas
    },

}