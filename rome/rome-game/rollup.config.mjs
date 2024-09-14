import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import serve from 'rollup-plugin-serve';
import livereload from 'rollup-plugin-livereload';
import url from '@rollup/plugin-url';

const dev = process.env.ROLLUP_WATCH;

export default {
  input: 'src/main.js',
  output: {
    file: 'dist/bundle.js',
    format: 'iife',
    name: 'RomeGame',
    sourcemap: true
  },
  plugins: [
    resolve(),
    commonjs(),
    url({
      include: ['**/*.png', '**/*.jpg', '**/*.gif', '**/*.svg'],
      limit: 0, // Always emit as separate files
      fileName: '[name][extname]'
    }),
    dev && serve({
      open: true,
      contentBase: ['dist', 'public'],
      port: 3000,
    }),
    dev && livereload('dist')
  ]
};