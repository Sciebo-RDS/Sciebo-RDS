import Vue from "rollup-plugin-vue"
import path from "path"
import serve from "rollup-plugin-serve"
import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import nodePolyfills from 'rollup-plugin-node-polyfills';
import replace from '@rollup/plugin-replace';

const dev = process.env.DEV === "true"

export default {
    input: path.resolve(__dirname, "src/index.js"),
    output: {
        name: "index.js",
        format: "amd",
        dir: "dist"
    },
    plugins: [
        Vue(),
        replace({
            preventAssignment: true,
            'process.env.NODE_ENV': JSON.stringify(dev ? 'production' : "development"),
        }),
        commonjs(),
        nodePolyfills(),
        nodeResolve({ browser: true, preferBuiltins: true }),
        dev && serve({
            contentBase: ["dist"],
            port: 8082
        }),
    ]
}