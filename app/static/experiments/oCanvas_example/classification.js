var classification = {

    start: function(params, next) {
        params['results'].push(['trial','block','stimId','category','response','accuracy','rt'])

        /*   initialize   */
        space = oCanvas.create({
            canvas: classification.initCanvas(),
            background: 'rgba(190,190,190,1)',
            // origin: { x: "center", y: "center" },
        })
        classification.initElements(params)

        x = new Date().getTime()
        rt = 0
        response = null
        acc = null
        trial = 0
        block = 0
        block_order = classification.generateBlockOrder(params['objects'], params['labels']) // <-- initialize the first block order (you'll do this every block)

        correctCategory = block_order[trial][1]
        classification.initStim(block_order[trial][0])

        space.scenes.load('selection')


        /*   define event logic   */
        for (category of params['categories']) {
            responseBtns[category].btn.bind('click tap', function () {
                rt = new Date().getTime() - x

                response = this.category
                acc = response == correctCategory

                if (acc == true) {
                    feedbackTxt.text = 'Yep! You got it. This is a member of category '.concat(params['btnLabels'][correctCategory])
                } else {
                    feedbackTxt.text = 'Sorry, that\'s not it. This is a member of category '.concat(params['btnLabels'][correctCategory])
                }

                space.scenes.unload('selection')
                space.scenes.load('feedback')

                setTimeout(function () {
                    space.scenes.load('continue')
                }, 200)
            })
        }


        continueBtn.bind('click tap', function () {
            space.scenes.unload('continue')
            space.scenes.unload('feedback')
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
                    block_order = classification.generateBlockOrder(params['objects'], params['labels'])
                }
            }

            setTimeout( function () {
                space.scenes.load('selection')
                classification.initStim(block_order[trial][0])
                correctCategory = block_order[trial][1]
                x = new Date().getTime()
            }, 200)

        })

        console.log('started classification')
    },


    initElements: function (params) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        /*   Response Phase of Trial   */
        responseBtns = {}
        btnCompression = .4
        for (let [index, category] of params['categories'].entries()) {
            let xpos = ((space.canvasElement.width / params['categories'].length) * index)  +  ((space.canvasElement.width / params['categories'].length) / 2)
            responseBtns[category] = {
                'category': category,
                'btnLabel': params['btnLabels'][category],
            }

            responseBtns[category].btn = space.display.rectangle({
                x: xpos + (((space.canvasElement.width / 2) - xpos) * btnCompression),
                y: centerY + 200,
                origin: { x: "center", y: "center" },// align: 'center',
                width: 160,
                height: 60,
                fill: "#079",
                stroke: "10px #079",
                join: "round",
                category: category, // <-- CAREFUL! This is a custom added property to the oCanvas Base object; if they decide to ever include it, this will overwrite whatever function they decide the 'category' property should have (though low odds of that happening)
            })
            responseBtns[category].btn.addChild(
                space.display.text({
                    x: 0,
                    y: 0,
                    origin: { x: "center", y: "center" },// align: 'center',
                    font: "bold 25px sans-serif",
                    text: responseBtns[category]['btnLabel'],
                    fill: "rgba(255,255,255,1)",
                    zIndex: "front",
                })
            )
        }

        instructionsTxt = space.display.text({
            x: centerX,
            y: centerY + 120,
            origin: { x: "center", y: "center" }, align: 'center',
            align: "center",
            font: "bold 25px sans-serif",
            text: "Which category do you think the item belongs to?",
            fill: "rgba(0,0,0,1)",
            zIndex: "front",
        })

        space.scenes.create('selection', function () {
            for (category of params['categories']) {
                this.add(responseBtns[category].btn)
            }
            this.add(instructionsTxt)
        })


        /*   Feedback   */
        if (params['feedback'] == true) {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy + 120,
                origin: { x: "center", y: "top" },
                font: "bold 30px sans-serif",
                text: "Feedback Message",
                fill: "#000000"
            });
        } else {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy,
                origin: { x: "center", y: "top" },
                font: "bold 30px sans-serif",
                text: " ",
                fill: "#000000"
            });
        }
        space.scenes.create('feedback', function () {
            this.add(feedbackTxt)
        })



        /*   Continue Button   */
        continueBtn = space.display.rectangle({
            x: cx,
            y: cy + 250,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })
        continueBtn.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Next Trial",
                fill: "rgba(255,255,255,1)",
                // zIndex: "front",
            })
        )
        space.scenes.create('continue', function () {
            this.add(continueBtn)
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
        idx = classification.shuffle([...Array(labels.length).keys()]) // from ben @ https://stackoverflow.com/a/10050831

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